__author__ = 'alexander'
import os

class Project:

    working_dir = ""
    data_dir = ""

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.data_dir = os.path.join(working_dir, "/data")
        if not os.path.exists(self.working_dir):
            os.mkdir(working_dir)

        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

    def savedata(self, data, filepath):
        with open(filepath, 'wb') as f:
            f.write(data)
