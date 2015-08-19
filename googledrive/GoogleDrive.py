from onlinestorage import OnlineStorage
from queue import Queue
from common import Common
import json
import urllib.parse
import webbrowser
from datetime import datetime, timedelta
from threading import Thread



class GoogleDrive(OnlineStorage.OnlineStorage):

    localstorage = None
    config = None
    token_endpoint = ""
    oauth_scope = ""
    oauth_endpoint = ""
    api_version = ""
    api_endpoint = ""
    redirect_uri = ""

    files = []

    client_id = ""
    client_secret = ""

    oauth = {"access_token" : "",
             "refresh_token": "",
             "expires_in:": 0}

    input_intercept = None
    config_intercept = None

    def __init__(self, config, localstorage, input_intercept, config_intercept):
        self.token_endpoint = config['token_endpoint']
        self.oauth_scope = config['oauth_scope']
        self.oauth_endpoint = config['oauth_endpoint']
        self.api_version = config['api_version']
        self.api_endpoint = config['api_endpoint']
        self.redirect_uri = config['redirect_uri']
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.input_intercept = input_intercept
        self.config_intercept = config_intercept
        self.files = []
        self.localstorage = localstorage

        super(GoogleDrive, self).__init__(self.api_endpoint, self.input_intercept, "Google_Drive")

    def _authorize(self):
        if not self.oauth['refresh_token']:
            # Step 1
            response_type = 'code'
            query_string =({'redirect_uri': self.redirect_uri,'response_type': response_type,'client_id': self.client_id,'scope': self.oauth_scope,'approval_prompt': 'force','access_type': 'offline'})
            params = urllib.parse.urlencode(query_string)
            step1 = self.oauth_endpoint + '?' + params
            try:
                webbrowser.open(step1)
            except:
                pass
            code = self.input_intercept('Authorization Code')

            # Step 2
            query_string = ({'code': code,'redirect_uri': self.redirect_uri,'client_id': self.client_id,'scope':'','client_secret': self.client_secret,'grant_type': 'authorization_code'})
            params = urllib.parse.urlencode(query_string)
            response = Common.webrequest(self.token_endpoint, {'content-type': 'application/x-www-form-urlencoded;charset=utf-8'}, self.http_intercept, params)
            json_response = json.loads(response)
            self._parse_token(json_response)
            self.config_intercept.save(self.oauth)
        else:
            self._refresh()
            self.config_intercept.save(self.oauth)

        t = Thread(target=self._refresh, args=({int(self.oauth['expires_in'])}))
        t.daemon = True
        t.start()

        #TODO: Logging here, access token etc

    def _refresh(self):
        query_string = ({'client_secret': self.client_secret,'grant_type': 'refresh_token','refresh_token': self.oauth['refresh_token'],'client_id': self.client_id})
        params = urllib.parse.urlencode(query_string)
        response = Common.webrequest(self.token_endpoint, {'content-type': 'application/x-www-form-urlencoded;charset=utf-8'}, self.http_intercept, params)
        json_response = json.loads(response)
        self._parse_token(json_response)

    def full_sync(self):
        # TODO: Logging here
        self.files = []
        self._get_items(Common.joinurl(self.api_endpoint, "files?maxResults=0"))
        cnt = len(self.files)
        # TODO: Log number of items to be synced

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
