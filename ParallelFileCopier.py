import os
import queue
import shutil
import threading
import time

from lib.ReadableSize import get_readable_size


class ParallelFileCopier:
    """
        A class used to copy files recursively from a source directory to a destination
        directory using multiple threads for improved performance.
        """

    def __init__(self, source_dir: str, destination_dir: str, number_of_threads: int):
        """
        Initializes the ParallelFileCopier with source/destination paths and thread configuration
            :param source_dir (str): The path to the source directory containing files to copy
            :param destination_dir (str): The path where files should be copied to
            :param number_of_threads (int): The number of concurrent worker threads to spawn
            """
        if not isinstance(source_dir, str):
            raise TypeError(f"Argument 'source_dir' must be a string")

        if not isinstance(destination_dir, str):
            raise TypeError(f"Argument 'destination_dir' must be a string")

        if not isinstance(number_of_threads, int):
            raise TypeError(f"Argument 'number_of_threads' must be an integer")

        if number_of_threads < 1:
            raise ValueError(f"Number of threads must be at least 1, got {number_of_threads}.")


        self.source_dir = source_dir
        self.destination_dir = destination_dir
        self.number_of_threads = number_of_threads

        if not os.path.exists(self.source_dir):
            raise FileNotFoundError(f"Source directory does not exist")

        if not os.path.isdir(self.source_dir):
            raise NotADirectoryError(f"Source path is not a directory")

        self.work_queue = queue.Queue()
        self.files_count = 0
        self.total_bytes = 0

    def _file_producer(self):
        """
        Internal method acting as the Producer.

        It traverses the source directory tree using os.walk(), calculates the total size
        of files found, and populates the work_queue with tuples of (source_path, dest_path).

        After all files are indexed, it inserts 'None' (poison pills) into the queue
        equal to the number of threads, signalling the consumers to terminate.
        """
        file_count = 0
        total_bytes = 0

        print(f"[Producer] Indexing files in: {self.source_dir}")

        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                source_path = os.path.join(root, file)

                try:
                    file_size = os.path.getsize(source_path)
                    total_bytes += file_size
                except OSError:
                    pass  # neni tolik potrebna informace, asi skipnem vyresime pozdeji

                relative_path = os.path.relpath(source_path, self.source_dir)
                dest_path = os.path.join(self.destination_dir, relative_path)

                self.work_queue.put((source_path, dest_path))
                file_count += 1

        readable_size = get_readable_size(total_bytes)
        print(f"[Producer] Found {file_count} files. Total size: {readable_size}")

        for every_thread in range(self.number_of_threads):
            self.work_queue.put(None)

    def _file_consumer(self, thread_id: int):
        """
        Internal method acting as the Consumer (Worker).

        Continuously fetches tasks from the work_queue. Each task is a tuple
        (src_path, dest_path). It ensures the destination directory exists
        and copies the file.

        The loop terminates when it encounters 'None' in the queue.

        :param thread_id (int): A unique identifier for the thread (used for logging).
        """
        while True:
            task = self.work_queue.get()

            if task is None:
                self.work_queue.task_done()
                break

            src_path, dest_path = task

            try:
                destination_folder = os.path.dirname(dest_path)

                os.makedirs(destination_folder, exist_ok=True)

                shutil.copy2(src_path, dest_path)

            except Exception as e:
                print(f"[Worker {thread_id}] ERROR copying {src_path}: {e}")

            self.work_queue.task_done()

    def start_copying(self):
        """
        Manages the copying process:

        Start X number of Consumer Threads
        Starts Producer thread to index files
        waits for producer to finish
        waits for queue to be empty
        waits for all consumer threads to terminate
        prints statistics and duration
        """
        start_time = time.time()
        threads = []

        print(f"Starting {self.number_of_threads} Worker Threads...")

        for i in range(self.number_of_threads):
            t = threading.Thread(target=self._file_consumer, args=(i + 1,))
            t.start()
            threads.append(t)

        print("Starting Producer Thread...")
        producer_thread = threading.Thread(target=self._file_producer)
        producer_thread.start()

        producer_thread.join()
        self.work_queue.join()

        for t in threads:
            t.join()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Done, total time = {duration:.2f} seconds")