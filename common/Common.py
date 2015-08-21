__author__ = 'aurcioli'
import urllib
import urllib.parse
from urllib.request import Request
from urllib import error

def safefilename(f):
    f = f.replace('\\', '_')
    f = f.replace('/', '_')
    f = f.replace('..','_')
    if len(f) > 100:
        f = f[:50] + '_'
    return f

def webrequest(url, headers, http_intercept, data=None, binary=False):

    # TODO: Add logging here

    try:
        headers['user-agent'] = "searchgiant forensic cli"
        if not data:
            # GET
            req = Request(url, None, headers)
            response = urllib.request.urlopen(req)
            if binary:
                return response.read()
            return response.read().decode('utf-8')
        else:
            # POST
            req = Request(url, data.encode('utf-8'), headers)
            response = urllib.request.urlopen(req)
            if binary:
                return response.read()
            return response.read().decode('utf-8')

    except urllib.error.HTTPError as err:
        http_intercept(err)
        webrequest(url, headers, http_intercept, data, binary)


def joinurl(b, p):
    if not b.endswith("/"):
        return urllib.parse.urljoin(b + "/", p)
    else:
        return urllib.parse.urljoin(b, p)



