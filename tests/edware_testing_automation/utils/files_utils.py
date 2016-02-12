import os
import time


class FileUtilsException(Exception):
    pass


def find_file(path, extension='.zip', timeout=20):
    end_time = time.time() + timeout

    while end_time >= time.time():
        for next_file in os.listdir(path):
            if next_file.endswith(extension):
                if path.endswith('/'):
                    return path + next_file
                else:
                    return path + '/' + next_file
        time.sleep(0.5)
    raise FileUtilsException(
            "Unable to find file with '{e}' extension by the following path: {path}".format(e=extension, path=path))
