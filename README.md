# Parallel File Copier

This project is a Python script designed for fast and efficient copying of large numbers of files recursively from a source directory to a destination directory. It implements the **Producer–Consumer** design pattern using **multithreading** to maximize I/O performance.

## 🚀 Features

- **Multithreading:** Utilizes multiple threads to copy files simultaneously (user-defined number of threads).
- **Producer–Consumer Pattern:**
  - **Producer:** A single thread efficiently traverses the directory tree and indexes files into a queue.
  - **Consumers:** A pool of worker threads picks up tasks from the queue and performs the actual copying.
- **Recursive Structure:** Handles nested folders and automatically mirrors the directory structure in the destination.
- **Metadata Preservation:** Uses `shutil.copy2`, ensuring copied files retain their original creation and modification timestamps.
- **Robustness:** Automatically creates missing target directories (`os.makedirs`).
- **Statistics:** Displays the total number of files found, their combined size, and the total execution time.

## 📂 Project Structure

- `main.py` – The entry point. Configures paths, initializes the copier, and handles execution.
- `ParallelFileCopier.py` – Contains the `ParallelFileCopier` class with the **Producer** and **Consumer** logic.
- `lib/ReadableSize.py` – Helper module to convert bytes into human-readable formats (KB, MB, GB).

## 🛠️ Requirements

- **Python 3.x**
- Standard libraries only (no `pip install` needed):
  - `os`, `queue`, `threading`, `time`, `shutil`

## ⚙️ Usage

1. **Clone or download** the repository.
2. **Open `main.py`** and configure your paths and thread count:

```python
from ParallelFileCopier import ParallelFileCopier

if __name__ == "__main__":
    # Configuration
    SOURCE = r"D:\Fotky"       # Source directory
    DESTINATION = r"D:\Test"   # Destination directory
    THREADS = 4                # Number of worker threads (usually CPU cores count)

    try:
        # Initialize and start the copier
        copier = ParallelFileCopier(SOURCE, DESTINATION, THREADS)
        copier.start_copying()

    except Exception as e:
        print(f"Error: {e}")