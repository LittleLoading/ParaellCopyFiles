# Parallel File Copier

This project is a Python script designed for fast and efficient copying of large numbers of files from one folder to another. It uses **multithreading** and the **Producer–Consumer** design pattern to maximize performance.

## 🚀 Features

- **Multithreading:** Utilizes multiple threads to copy files simultaneously (default: 40 threads).
- **Producer–Consumer Pattern:**
  - **Producer:** A single thread quickly indexes files and pushes them into a queue.
  - **Consumers:** A pool of worker threads takes tasks from the queue and performs the actual copying.
- **Metadata Preservation:** Uses `shutil.copy2`, ensuring copied files keep their original creation and modification timestamps.
- **Robustness:** Automatically creates missing target directories.
- **Statistics:** Displays the total number of files found, their combined size, and the total processing time.

## 📂 Project Structure

- `main.py` – The main entry point. Configures paths, starts threads, and measures execution time.
- `FileManager.py` – Contains logic for the **Producer** (file discovery) and **Consumer** (copying).
- `lib/ReadableSize.py` – Helper function that converts bytes into a human-readable format (KB, MB, GB...).

## 🛠️ Requirements

- Python 3.x  
- Standard libraries only (no pip installations needed):  
  `os`, `queue`, `threading`, `time`, `shutil`

## ⚙️ Configuration

Before running the script, configure the source and destination directories in `main.py`:

```python
# main.py

source_dir = r"D:\Fotky"       # Path to the source folder
destination_dir = r"D:\Test"   # Path where files will be copied
number_of_threads = 40         # Number of worker threads
