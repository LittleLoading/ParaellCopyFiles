from ParallelFileCopier import ParallelFileCopier
from ConfigurationLoader import load_config
from Logger import Logger

if __name__ == "__main__":
    config = load_config()

    source = config.get("source")
    destination = config.get("destination")
    threads = config.get("threads",4)
    log_file = config.get("log_file", "logs/app.log")

    if not source or not destination:
        raise Exception("Source and destination are not defined")

    logger = Logger(log_file)


    try:
        copier = ParallelFileCopier(source, destination, threads,logger)

        copier.start_copying()

    except Exception as e:
        print(f"Error: {e}")