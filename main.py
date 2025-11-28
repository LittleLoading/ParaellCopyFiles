import os
import queue
import threading
import time
from FileManager import file_producer
from FileManager import file_consumer


if __name__ == "__main__":
    source_dir = r"D:\Fotky"
    destination_dir = r"D:\Test"
    number_of_threads = 4

    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        raise Exception("Source directory does not exist.")
    work_queue = queue.Queue()

    start_time = time.time()
    threads = []

    print(f"Starting {number_of_threads} Worker Threads...")

    for i in range(number_of_threads):
        t = threading.Thread(target=file_consumer, args=(i + 1, work_queue))
        t.start()
        threads.append(t)

    print("Starting Producer Thread...")
    producer_thread = threading.Thread(
        target=file_producer,
        args=(source_dir, destination_dir, work_queue, number_of_threads)
    )
    producer_thread.start()

    producer_thread.join()

    work_queue.join()

    for t in threads:
        t.join()

    end_time = time.time()
    duration = end_time - start_time

    print(f"Done, total time = {duration:.2f} seconds")
