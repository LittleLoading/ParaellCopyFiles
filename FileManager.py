import os
import shutil

from lib.ReadableSize import get_readable_size

def file_producer(source_dir, destination_dir, work_queue, num_threads):
    """
    Goes through source directory and pastes (source_path, destination_path) into queue, than ends threads
    :param source_dir: path to source directory
    :param destination_dir: path to destination directory
    :param work_queue: shared queue for threads managing
    :param num_threads: number of threads
    :return:
    """
    file_count = 0
    total_bytes = 0

    print(f"[Producer] Indexing files in: {source_dir}")

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_path = os.path.join(root, file)

            try:
                file_size = os.path.getsize(source_path)
                total_bytes += file_size
            except OSError:
                pass #neni tolik potrebna informace, asi skipnem vyresime pozdeji

            relative_path = os.path.relpath(source_path, source_dir)
            dest_path = os.path.join(destination_dir, relative_path)

            work_queue.put((source_path, dest_path))
            file_count += 1

    readable_size = get_readable_size(total_bytes)
    print(f"[Producer] Found {file_count} files. Total size: {readable_size}")

    for every_thread in range(num_threads):
        work_queue.put(None)


def file_consumer(thread_id, work_queue):
    """
    Gets task from work queue  (source path and destination path) and copyes the file.
    :param thread_id: int id of thread to manage them
    :param work_queue: shared queue where threads get paths to source path and destination path of files
    :return:
    """
    while True:
        task = work_queue.get()

        if task is None:
            work_queue.task_done()
            break

        src_path, dest_path = task

        try:
            destination_folder = os.path.dirname(dest_path)

            os.makedirs(destination_folder, exist_ok=True)

            shutil.copy2(src_path, dest_path)

        except Exception as e:
            print(f"[Worker {thread_id}] ERROR copying {src_path}: {e}")

        work_queue.task_done()

