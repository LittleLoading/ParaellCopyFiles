import os
import queue
import shutil
import multiprocessing
import time


from lib.ReadableSize import get_readable_size
from Logger import Logger

class ParallelFileCopier:
    """
        A class used to copy files recursively from a source directory to a destination
        directory using multiple PROCESSES for improved performance.
        """

    def __init__(self, source_dir: str, destination_dir: str, number_of_processes: int, logger: Logger):
        """
        Initializes the ParallelFileCopier with source/destination paths and processes configuration
            :param source_dir (str): The path to the source directory containing files to copy
            :param destination_dir (str): The path where files should be copied to
            :param number_of_processes (int): The number of concurrent worker processes to spawn
            """
        if not isinstance(source_dir, str):
            raise TypeError(f"Argument 'source_dir' must be a string")

        if not isinstance(destination_dir, str):
            raise TypeError(f"Argument 'destination_dir' must be a string")

        if not isinstance(number_of_processes, int):
            raise TypeError(f"Argument 'number_of_processes' must be an integer")

        if number_of_processes < 1:
            raise ValueError(f"Number of processes must be at least 1, got {number_of_processes}.")


        self.source_dir = source_dir
        self.destination_dir = destination_dir
        self.number_of_processes = number_of_processes
        self.logger = logger

        if not os.path.exists(self.source_dir):
            raise FileNotFoundError(f"Source directory does not exist")

        if not os.path.isdir(self.source_dir):
            raise NotADirectoryError(f"Source path is not a directory")

        self.work_queue = multiprocessing.JoinableQueue()
        self.files_count = 0
        self.total_bytes = 0

    def _file_producer(self):
        """
        Internal method acting as the Producer.

        It traverses the source directory tree using os.walk(), calculates the total size
        of files found, and populates the work_queue with tuples of (source_path, dest_path).

        After all files are indexed, it inserts 'None' (poison pills) into the queue
        equal to the number of processes, signalling the consumers to terminate.
        """
        file_count = 0
        total_bytes = 0

        #print(f"[Producer] Indexing files in: {self.source_dir}")
        self.logger.write_info(f"[Producer] Indexing files in: {self.source_dir}")

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
        #print(f"[Producer] Found {file_count} files. Total size: {readable_size}")
        self.logger.write_info(f"[Producer] Found {file_count} files. Total size: {readable_size}")

        for every_process in range(self.number_of_processes):
            self.work_queue.put(None)

    def _file_consumer(self, process_id: int):
        """
        Internal method acting as the Consumer (Worker).

        Continuously fetches tasks from the work_queue. Each task is a tuple
        (src_path, dest_path). It ensures the destination directory exists
        and copies the file.

        The loop terminates when it encounters 'None' in the queue.

        :param process_id (int): A unique identifier for the process (used for logging).
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
                #print(f"[Worker {process_id}] ERROR copying {src_path}: {e}")
                self.logger.write_error(f"[Worker {process_id}] ERROR copying {src_path}: {e}")
            self.work_queue.task_done()

    def start_copying(self):
        """
        Manages the copying process:

        Start X number of Consumer Processes
        Starts Producer Process to index files
        waits for producer to finish
        waits for queue to be empty
        waits for all consumer process to terminate
        prints statistics and duration
        """
        start_time = time.time()
        processes = []

       # print(f"Starting {self.number_of_processes} Worker Processes...")
        self.logger.write_info(f"Starting {self.number_of_processes} Worker Processes...")

        for i in range(self.number_of_processes):
            p = multiprocessing.Process(target=self._file_consumer, args=(i + 1,))
            p.start()
            processes.append(p)

        #print("Starting Producer Process...")
        self.logger.write_info("Starting Producer Process...")
        producer_proces = multiprocessing.Process(target=self._file_producer)
        producer_proces.start()

        producer_proces.join()
        self.work_queue.join()

        for p in processes:
            p.join()

        end_time = time.time()
        duration = end_time - start_time

        #print(f"Done, total time = {duration:.2f} seconds")
        self.logger.write_info(f"Done, total time = {duration:.2f} seconds")
