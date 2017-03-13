#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: hackqiang
# version 0.1
# requirement: python2.7 flask 
'''
    process chart: https://www.processon.com/view/link/5826fc4be4b00c4fc8803330
    


'''
import os
import sys
from flask import Flask, render_template, request, Response

from filter import *

app = Flask(__name__)

filters = {}
filters['mt'] = 'https://tp.m-team.cc/torrentrss.php?https=1&rows=10&cat421=1&linktype=dl&passkey=62663ec0b703fe11c7df6872d49a793a&isize=1'
filters['hdhome'] = 'http://hdhome.org/torrentrss.php?rows=10&cat414=1&linktype=dl&passkey=0f9d0b335d0a61ebd2f4ff57cf7a8c1c&isize=1'
#filters['u2'] = 'https://u2.dmhy.org/torrentrss.php?rows=10&cat12=1&passkey=80150a16d3f0805c2f9493851726d70a&linktype=dl&passkey=80150a16d3f0805c2f9493851726d70a'


@app.route("/")
def hello():
    return "Hello RSS!"
    
@app.route("/rss")
def rss():
    '''
        http://192.168.1.2:4201/rss?filter=mt
    '''
    return Response(rss_filter(filters[request.args.get('filter')]), mimetype='text/xml')

if __name__ == "__main__":
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    

    app.run(host = '0.0.0.0', port = 4201)