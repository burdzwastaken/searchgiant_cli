__author__ = 'aurcioli'
import urllib
import urllib.parse
from urllib.request import Request
from urllib import error

def webrequest(url, headers, http_intercept, data = None):
    #TODO: Add logging here
    try:
        headers['user-agent'] = "searchgiant forensic cli"
        if (data == None):
            # GET
            req = Request(url, None, headers)
            response = urllib.request.urlopen(req)
            return response.read().decode('utf-8')
        else:
            # POST
            req = Request(url, data.encode('utf-8'), headers)
            response = urllib.request.urlopen(req)
            return response.read().decode('utf-8')

    except urllib.error.HTTPError as err:
        http_intercept(err)
        webrequest(url, headers, http_intercept, data)


def joinurl(b, p):
    if (b.endswith("/") == False):
        return urllib.parse.urljoin(b + "/", p)
    else:
        return urllib.parse.urljoin(b, p)



