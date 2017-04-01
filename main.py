#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: hackqiang
# version 0.1
# requirement: python2.7 
# pip install flask apscheduler 

import os
import threading
import time
import sys
import logging
import logging.handlers
from collections import OrderedDict
from flask import Flask, render_template, request, Response
from apscheduler.schedulers.background import BackgroundScheduler
#from gevent import monkey
#monkey.patch_all()

reload(sys)
sys.setdefaultencoding('utf8')

from PThtmlparser import PThtmlparser

app = Flask(__name__)

hostlist_index_type    = 0
hostlist_index_https   = 1
hostlist_index_parser  = 2
hostlist_index_info    = 3
hostlist_index_search_result  = 4

'''
    hostlist = list(type, https, parser, info)
    info = (update_time, upload, download, coins)
'''
hostlist = OrderedDict()
hostlist['tp.m-team.cc'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['totheglory.im'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['hdsky.me'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['u2.dmhy.org'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['hdcmct.org'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['chdbits.co'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['hdhome.org'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['www.hyperay.org'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['pt.upxin.net'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['www.hdpter.net'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['pt.keepfrds.com'] = list(('NexusPHP', True, None, None, 'no'))
hostlist['pt.gztown.net'] = list(('NexusPHP', False, None, None, 'no'))
hostlist['tthd.org'] = list(('NexusPHP', False, None, None, 'no'))


def search_worker(host, keywords):
    logging.debug('sign_in_worker call')
    hostlist[host][hostlist_index_search_result] = hostlist[host][hostlist_index_parser].search(keywords)

@app.route("/")
def index():
    keywords = request.args.get('search')
    if keywords:
        res = ''
        for (host, host_info) in hostlist.items():
            logging.info('init %s' % host)
            t = threading.Thread(target=search_worker, args=[host, keywords])
            t.setDaemon(True)
            t.start()

        all_finish = False
        while not all_finish:
            for (host, host_info) in hostlist.items():
                if host_info[hostlist_index_search_result] != 'no':
                    all_finish = True
                else:
                    all_finish = False
                    time.sleep(0.5)
                    break

        for (host, host_info) in hostlist.items():
            res += hostlist[host][hostlist_index_search_result]
            hostlist[host][hostlist_index_search_result] = 'no'
        return res
    else:
        infos = list()
        for (host, host_info) in hostlist.items():
            if host_info[hostlist_index_parser]:
                info = list()
                info.append(host)
                info.append(host_info[hostlist_index_https])
                info.extend(host_info[hostlist_index_info])
                infos.append(info)
            # host, data, update_time
        return render_template('index.html', infos=infos)
    

@app.route("/rss")
def rss():
    '''
        http://192.168.1.2:4201/rss?filter=mt
    '''
    return Response(rss_filter(filters[request.args.get('filter')]), mimetype='text/xml')


def update_user_info_worker(worker, host_info):
    logging.debug('update_user_info_worker call')
    (ret, upload, download, coins) = worker()
    update_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
    host_info[hostlist_index_info] = list((update_time, upload, download, coins))


def sign_in_worker(worker):
    logging.debug('sign_in_worker call')
    worker()

    
if __name__ == "__main__":
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists('log'):
        os.mkdir('log')
    
    logging.basicConfig(level=logging.DEBUG) 
    handler = logging.handlers.RotatingFileHandler('log/main.log', maxBytes=1024*1024*10, backupCount=0)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(handler)

    scheduler = BackgroundScheduler()
    
    for (host, host_info) in hostlist.items():
        logging.info('init %s' % host)
        try:
            hostlist[host][hostlist_index_parser] = PThtmlparser.PThtmlparser(host, host_info[0], host_info[1])
        except Exception as e:
            logging.error(e)
            hostlist[host][hostlist_index_parser] = None
        hostlist[host][hostlist_index_info] = list(('Never', '', '', ''))
        
        parser = host_info[hostlist_index_parser]
        #scheduler.add_job(update_user_info_worker, 'interval', minutes=360, args=[parser.get_user_info, host_info])
        scheduler.add_job(update_user_info_worker, 'cron', hour='6,8,10,12,16,18,20,21,22,23', args=[parser.get_user_info, host_info])
        scheduler.add_job(sign_in_worker, 'cron', second='0,10,20', minute='0', hour='0,23', args=[parser.signin])

        #run immediatlly
        thread = threading.Thread(target=update_user_info_worker, args=[parser.get_user_info, host_info])
        thread.setDaemon(True)
        thread.start()
        thread = threading.Thread(target=sign_in_worker, args=[parser.signin])
        thread.setDaemon(True)
        thread.start()

    scheduler.start()
        
    app.run(host='127.0.0.1', port=4201, threaded=True, debug=False)
