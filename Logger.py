import datetime
import logging
import os.path


class Logger:
    def __init__(self,path_file):
        self.path = None

        if not path_file or not isinstance(path_file, str):
            print("LOGGER WARNING: Path to log is not type  string. Logging to file is off.")
            return

        try:
            directory = os.path.dirname((path_file))
            if directory and not os.path.exists(directory):
                os.makedirs(directory,exist_ok=True)

                self.path = path_file
        except OSError as e:
            print(f"Logger Error: Cant create dir for logs {e}")
            self.path  = None




    def _write_log(self,type,message):
        try:
            time = datetime.datetime.now().strftime("%H:%M:%S")

            row = f"{time} | {type} | {str(message)} "

            print(row)

            if self.path:
                with open(self.path, "a", encoding='utf-8') as file:
                    file.write(row + '\n')
        except Exception as e:
            print(f"LOGGER WRITE FAILURE: Cant write into file: {e}")

    def write_info(self,message):
        self._write_log("INFO", message)

    def write_error(self,message):
        self._write_log("ERROR",message)
