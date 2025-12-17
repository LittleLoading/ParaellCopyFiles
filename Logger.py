import datetime
import logging
import os.path


class Logger:
    """
    Class that handles logging. Writes log messages to both console and specified log file
    """
    def __init__(self,path_file):
        """
        Inicialize logging and check if path to file exists, if not it creates a new one
        :param path_file: path to logging file example 'logs/app.log'
        """
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
        """
        Method to handle formatting and writing of logs
        it formats timestamp, prints message to console and appends it to log file (if exists)

        :param type: str type of log (INFORMATION/ERROR....)
        :param message: str message to log
        """
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
        """
        Logs an informational message
        :param message: information to log
        """
        self._write_log("INFO", message)

    def write_error(self,message):
        """
        Logs an Error message
        :param message: error detail;s to log
        """
        self._write_log("ERROR",message)
