__author__ = 'alexander'
import os
import logging
from logging import FileHandler
from config import ConfigLoader
from oi.IO import IO
import time

class DefaultConfigs:
    defaults = {"Google_Drive":
                    ("TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'\r\n"
                     "OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'\r\n"
                     "OAUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'\r\n"
                     "API_VERSION = 'v2'\r\n"
                     "API_ENDPOINT = 'https://www.googleapis.com/drive/v2'\r\n"
                     "REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'\r\n"
                     "CLIENT_ID = ''\r\n"
                     "CLIENT_SECRET = ''\r\n"
                     "THREADS = 3\r\n")
                }


class Project:

    working_dir = ""
    data_dir = ""
    log_dir = ""
    transaction_log = ""
    exception_log = ""
    metadata_file= ""
    config = None
    transaction_logger = None
    exception_logger = None
    name = ""

    def __init__(self, working_dir, project_name):
        self.name = project_name
        self.working_dir = os.path.join(working_dir, self.name)
        self.data_dir = os.path.join(self.working_dir, "data")
        self.log_dir = os.path.join(self.working_dir, "logs")
        self.config_file = os.path.join(self.working_dir, "config.cfg")
        IO.put("Initializing project in " + self.working_dir, "highlight")
        IO.put("Data path is " + self.data_dir)
        IO.put("Log path is " + self.log_dir)
        IO.put("Config file is " + self.config_file)

        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir, exist_ok=True)
            os.makedirs(self.data_dir, exist_ok=True)
            os.makedirs(self.log_dir, exist_ok=True)
            IO.put("Working directory not found, creating from scratch", "warn")

        if not os.path.isfile(self.config_file):
            IO.put("Config file not found, creating default config file", "warn")
            with open(self.config_file, 'w') as f:
                f.write(DefaultConfigs.defaults[self.name])

        self.config = ConfigLoader.ConfigLoader()
        self.config.from_file(self.config_file)

        self.transaction_log = os.path.join(self.log_dir, "transaction.log")
        self.exception_log = os.path.join(self.exception_log, "exception.log")
        self.metadata_file = os.path.join(self.working_dir, "metadata.csv")

        self.transaction_logger = logging.getLogger(project_name + "_t")
        self.exception_logger = logging.getLogger(project_name + "_e")

        tfh = FileHandler(self.transaction_log)
        efh = FileHandler(self.exception_log)

        fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fmt.converter = time.gmtime
        tfh.setFormatter(fmt)
        efh.setFormatter(fmt)

        self.transaction_logger.addHandler(tfh)
        self.exception_logger.addHandler(efh)

    def log(self, type, message, level, stdout=False):

        levels = {}
        levels['info'] = 20
        levels['warning'] = 30
        levels['error'] = 40
        levels['critical'] = 50
        levels['highlight'] = 20

        if stdout:
            IO.put(message, level)

        if type.lower() == "exception":
            self.exception_logger.log(level, message)

        self.transaction_logger.log(levels[level], message)

    def save(self, key, value):
        self.config.from_file(self.config_file)
        self.config[key] = value
        with open(self.config_file,'w') as f:
            for k,v in self.config.items():
                if type(v) is str:
                    f.write('{}="{}"\n'.format(k.upper(),v))
                else:
                    f.write('{}={}\n'.format(k.upper(),v))
        self.config.from_file(self.config_file)

    def savedata(self, data, filepath):
        with open(filepath, 'wb') as f:
            f.write(data)
