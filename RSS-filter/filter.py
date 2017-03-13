#!/usr/bin/env python
# -*- coding=utf-8 -*-

import urllib2
import sys
import time
import re
from xml.etree.ElementTree import ElementTree,Element

def url_get(url):
    html = None
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
        handle = urllib2.urlopen(req, data=None, timeout = 10)
          
        html = handle.read()
        receive_header = handle.info()
    except Exception as e:
        print e
    #html = html.decode('utf-8').encode(sys.getfilesystemencoding())
    #print receive_header
    #print '#####################################'
    #print html
    return html

def check_size(size):
    return True

def get_size(title):
    size = 0.0

    m = re.search('\[(\d*\.\d* [GM]B)\]', title)
    if m:
        str_size = m.group(1)
        size = float(str_size.split(' ')[0])
        unit = str_size.split(' ')[1]
        if unit == 'GB':
            size *= 1024
    print size
    
    return size
    
def rss_filter(rss_url):
    '''
        1. get Origin RSS XML
        2. GET detail page
        3. check size
        4. check free flag
        5. return XML buffer
    '''
    for i in range(3):
        buf = url_get(rss_url)
        if buf:
            origin_xml_path = time.strftime("tmp/%y%m%d_%H%M%S_origin.xml")
            #origin_xml_path = 'tmp/161112_131139_origin.xml'
            output_xml_path = time.strftime("tmp/%y%m%d_%H%M%S_output.xml")
            try:
                file = open(origin_xml_path, 'w')
                file.write(buf)
                file.close()
                
                tree = ElementTree()
                tree.parse(origin_xml_path)
                
                node_channel = tree.find('channel')
                for node_item in node_channel.findall('item'):
                    details_url = node_item.find('link').text
                    title = node_item.find('title').text
                    size = get_size(title)
                    if not check_size(size):
                        node_channel.remove(node_item)
                
                tree.write(output_xml_path, encoding = "utf-8", xml_declaration = True)
                
                file = open(output_xml_path, 'r')
                xml_buf = file.read()
                file.close()
                    
            except Exception as e:
                print e
                
            return xml_buf
    
    return None
    