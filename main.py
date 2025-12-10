from ParallelFileCopier import ParallelFileCopier
from ConfigurationLoader import load_config

if __name__ == "__main__":
    config = load_config()

    source = config.get("source")
    destination = config.get("destination")
    threads = config.get("threads",4)

    if not source or not destination:
        raise Exception("Source and destination are not defined")

    try:
        copier = ParallelFileCopier(source, destination, threads)

        copier.start_copying()

    except Exception as e:
        print(f"Error: {e}")