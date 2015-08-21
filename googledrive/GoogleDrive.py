from onlinestorage import OnlineStorage
from common import Common
import json
import urllib.parse
import webbrowser
from datetime import datetime, timedelta
from threading import Thread
from downloader import Downloader
import os


class GoogleDrive(OnlineStorage.OnlineStorage):

    token_endpoint = ""
    oauth_scope = ""
    oauth_endpoint = ""
    api_version = ""
    api_endpoint = ""
    redirect_uri = ""

    files = []

    client_id = ""
    client_secret = ""

    oauth = {"access_token": "",
             "refresh_token": "",
             "expires_in:": 0}

    input_callback = None
    config_callback = None

    def __init__(self, project, input_callback, config_callback):
        self.project = project
        config = self.project.config
        self.token_endpoint = config['token_endpoint']
        self.oauth_scope = config['oauth_scope']
        self.oauth_endpoint = config['oauth_endpoint']
        self.api_version = config['api_version']
        self.api_endpoint = config['api_endpoint']
        self.redirect_uri = config['redirect_uri']
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.input_callback = input_callback
        self.config_callback = config_callback
        self.files = []
        super(GoogleDrive, self).__init__(self.api_endpoint, self.input_callback, "Google_Drive")

    def _authorize(self):
        if not self.oauth['refresh_token']:
            # Step 1
            response_type = 'code'
            query_string = (
            {'redirect_uri': self.redirect_uri, 'response_type': response_type, 'client_id': self.client_id,
             'scope': self.oauth_scope, 'approval_prompt': 'force', 'access_type': 'offline'})
            params = urllib.parse.urlencode(query_string)
            step1 = self.oauth_endpoint + '?' + params
            try:
                webbrowser.open(step1)
            except:
                pass
            code = self.input_callback('Authorization Code')

            # Step 2
            query_string = ({'code': code, 'redirect_uri': self.redirect_uri, 'client_id': self.client_id, 'scope': '',
                             'client_secret': self.client_secret, 'grant_type': 'authorization_code'})
            params = urllib.parse.urlencode(query_string)
            response = Common.webrequest(self.token_endpoint,
                                         {'content-type': 'application/x-www-form-urlencoded;charset=utf-8'},
                                         self.http_intercept, params)
            json_response = json.loads(response)
            self._parse_token(json_response)
            self.config_callback.save(self.oauth)
        else:
            self._refresh()
            self.config_callback.save(self.oauth)

        t = Thread(target=self._refresh, args=({int(self.oauth['expires_in'])}))
        t.daemon = True
        t.start()

        # TODO: Logging here, access token etc

    def _refresh(self):
        query_string = ({'client_secret': self.client_secret, 'grant_type': 'refresh_token',
                         'refresh_token': self.oauth['refresh_token'], 'client_id': self.client_id})
        params = urllib.parse.urlencode(query_string)
        response = Common.webrequest(self.token_endpoint,
                                     {'content-type': 'application/x-www-form-urlencoded;charset=utf-8'},
                                     self.http_intercept, params)
        json_response = json.loads(response)
        self._parse_token(json_response)

    def full_sync(self):
        # TODO: Logging here
        self.files = []
        self._get_items(Common.joinurl(self.api_endpoint, "files?maxResults=0"))
        cnt = len(self.files)
        # TODO: Log number of items to be synced
        d = Downloader.Downloader(self.http_intercept, self._save_file, self.get_auth_header, int(self.project.config['threads']))
        for file in self.files:
            parentmap = self._get_parent_mapping(file, self.files)
            path_to_create = os.normpath(os.path.join(path_to_create, parentmap))
            filetitle = Common.safefilename(file['title'])

            download_uri = self._get_download_url(file)
            d.put(Downloader.DownloadSlip(download_uri, file))
        d.start()

    def _save_file(self, data, file):
        parentmap = self._get_parent_mapping(file, self.files)
        path_to_create = os.path.normpath(os.path.join(self.project.data_dir, parentmap))
        filetitle = Common.safefilename(file['title'])

        if filetitle != file['title']:
            #TODO LOG Warning normalized filename from .. to ..
            pass

        savepath = os.path.join(path_to_create, filetitle)

        if len(path_to_create) > 255:
            # TODO: Log path name is too long
            pass
        else:
            if not os.path.isdir(path_to_create):
                os.makedirs(path_to_create, exist_ok=True)

        if len(filetitle) > 255:
            # TODO LOG path name is too long
            pass
        else:
            if data:
                self.project.savedata(data, savepath)
            else:
                # TODO: Download metadata only
                pass

    def _get_parent_mapping(self, i, items):
        # This is the secret sauce
        folderpath = ""
        while 'parents' in i or len(i['parents']) != 0:
            for p in i['parents']:
                if p['isRoot'] == True:
                    return folderpath
                else:
                    item = self._get_item_by_id(p['id'], items)
                    if item is not None:
                        folderpath = os.path.join(self._get_parent_mapping(item, items), item['title'])
                        return folderpath
                    else:
                        return folderpath

    def _get_item_by_id(self, f_id, items):
        for i in items:
            if i['id'] == f_id:
                return i
        return None

    def _get_download_url(self, file):
        preferred = "application/pdf"
        if 'downloadUrl' in file:
            return file['downloadUrl']
        if 'exportLinks' in file:
            if preferred in file['exportLinks']:
                return file['exportLinks'][preferred]
        else:
            return file[0]
        return None

    def get_auth_header(self):
        return {'Authorization': 'Bearer ' + self.oauth['access_token']}

    def _get_items(self, link):
        response = Common.webrequest(link, self.get_auth_header(), self.http_intercept)
        json_response = json.loads(response)
        if 'nextLink' in json_response:
            items = json_response['items']
            self._add_items_to_files(items)
            self._get_items(json_response['nextLink'])
        else:
            items = json_response['items']
            self._add_items_to_files(items)

    def _add_items_to_files(self, items):
        for i in items:
            self.files.append(i)

    def _parse_token(self, response):
        self.oauth['access_token'] = response['access_token']
        self.oauth['expires_in'] = response['expires_in']
        self.oauth['expire_time'] = datetime.utcnow() + timedelta(0, int(self.oauth['expires_in']))
        if 'refresh_token' in response:
            self.oauth['refresh_token'] = response['refresh_token']

    def http_intercept(self, err, req):
        if err.code == 401:
            # TODO: Reauthorize, and log
            self._authorize()
        else:
            # TODO: Log error
            pass
