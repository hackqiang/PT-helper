import os
import sqlite3
import cookielib
import Cookie
import urllib2
import urllib
import json
import logging

http_timeout = 30


def get_cookie(host):
    # cookie from EditThisCookie
    cookie = cookielib.MozillaCookieJar()
    try:
        cookies = open('data/cookies/%s' % host).read()
    except Exception,e:
        logging.error('can not read data/cookies/%s' % host)
        return None
        
    for item in json.loads(cookies):
        cookie.set_cookie(cookielib.Cookie(version=0, name=item['name'], value=item['value'], port=None, port_specified=False, domain=item['domain'], domain_specified=False, domain_initial_dot=False, path=item['path'], path_specified=True, secure=item['secure'], expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False))

    return cookie


def get_page(cookie, url, data=None):
    html = ''
    try:
        logging.info('request %s' % url)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')]
        if data:
            data = urllib.urlencode(data)
            html = opener.open(url, data, timeout = http_timeout).read()
        else:
            html = opener.open(url, timeout = http_timeout).read()
    except Exception as e:
        logging.error(e)
    return html
