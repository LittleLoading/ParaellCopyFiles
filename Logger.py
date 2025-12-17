import datetime
import logging
import os.path


class Logger:
    def __init__(self,path_file):
        self.path = path_file

        directory = os.path.dirname((path_file))
        if directory and not os.path.exists(directory):
            os.makedirs(directory)


    def _write_log(self,type,message):

        time = datetime.datetime.now().strftime("%H:%M:%S")

        row = f"{time} [{type},{message}]"

        print(row)

        with open(self.path, "a") as file:
            file.write(row + '\n')


    def write_info(self,message):
        self._write_log("INFO", message)

    def write_error(self,message):
        self._write_log("ERROR",message)
