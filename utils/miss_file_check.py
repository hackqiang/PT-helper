#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: hackqiang
# version 0.1
# requirement: python2.7

import os


torrents_path = '/var/lib/transmission-daemon/info/torrents'
download_path = '/media'

torents_list = list()
miss_list = list()

def get_torents_list():
    for root, dirs, files in os.walk(torrents_path):
        for file in files:
            torents_list.append(file[:-len('.ac112a0ed06e5a0e.torrent')])
    
    #print torents_list
        
if __name__ == "__main__":
    get_torents_list()
    #exit(0)
    
    for root, dirs, files in os.walk(download_path):
        for file in files:
            file_name = os.path.join(root, file)
            miss_list.append(file_name)
            for f in torents_list:
                if f in file_name:
                    miss_list.pop()
                    break
    with open('missing.log', 'w') as f:  
        for miss in miss_list:
            print miss
            f.write(miss+'\n')
            
                    