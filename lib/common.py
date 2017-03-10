#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import httplib
import json
from urlparse import urlparse


def run_request(url, method, commparams={}, options={}):
    urls = urlparse(url)
    host = urls.netloc
    path = urls.path

    header = {}
    if options == {}:
        header = {'Accept': 'application/json', 'Content-Type': 'application/Text'}
    else:
        header = options
        if not options.has_key("accept"):
            header['Accept'] = 'application/json'
        else:
            header['Accept'] = options['Accept']

        if not options.has_key('Content-Type'):
            header['Content-Type'] = 'application/json'
        else:
            header['Content-Type'] = options['Content-Type']

    if urls.scheme == "http":
        conn = httplib.HTTPConnection(host)
    else:
        conn = httplib.HTTPSConnection(host)
    if commparams:
        commparams = json.dumps(commparams)
        conn.request(method, path, commparams, headers=header)
    else:
        conn.request(method, path, headers=header)
    res = conn.getresponse()
    respone = res.read()
    conn.close()
    return res.status, respone


