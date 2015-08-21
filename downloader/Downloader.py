__author__ = 'alexander'
from queue import Queue
from common import Common
from threading import Thread

class DownloadSlip:

    def __init__(self, url, item):
        self.url = url
        self.item = item


class Downloader(Queue):

    headers = ""
    storage_callback = None
    threads = 3

    def __init__(self, http_callback, storage_callback, headers, threads):

        self.headers = headers
        self.storage_callback = storage_callback
        self.threads = threads
        self.http_callback = http_callback
        super(Downloader, self).__init__()

    def start(self):
        for i in range(0, self.threads):
            t = Thread(target=self._downloader)
            t.daemon = True
            t.start()
            # TODO: Log spinning up download threads

    def _downloader(self):
        while not self.empty():
            slip = self.get()
            file_item = slip.item
            file_url = slip.url
            data = Common.webrequest(file_url, self.headers, self.http_callback, None, True)
            # TODO: Log downloading file
            self.storage_callback(data, file_item)



