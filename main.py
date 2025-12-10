from ParallelFileCopier import ParallelFileCopier


if __name__ == "__main__":

    SOURCE = r"D:\\Fotku"
    DESTINATION = r"D:\\Test"
    THREADS = 4

    try:
        copier = ParallelFileCopier(SOURCE, DESTINATION, THREADS)

        copier.start_copying()

    except Exception as e:
        print(f"Error: {e}")