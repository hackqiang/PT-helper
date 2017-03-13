#!/usr/bin/python
# -*- coding=utf-8 -*-
# author : wklken@yeah.net
# date: 2012-05-25
# version: 0.1

import time
from xml.etree.ElementTree import ElementTree,Element
import re



def get_size():
    size = 0.0
    
    text = "asdasd [45.48 GB]"
    m = re.search('\[(\d*\.\d* [GM]B)\]', text)
    if m:
        str_size = m.group(1)
        size = float(str_size.split(' ')[0])
        unit = str_size.split(' ')[1]
        if unit == 'GB':
            size *= 1024
    print size
    
    return size

def read_xml(in_path):
  '''��ȡ������xml�ļ�
    in_path: xml·��
    return: ElementTree'''
  tree = ElementTree()
  tree.parse(in_path)
  return tree

def write_xml(tree, out_path):
  '''��xml�ļ�д��
    tree: xml��
    out_path: д��·��'''
  tree.write(out_path, encoding="utf-8",xml_declaration=True)

def if_match(node, kv_map):
  '''�ж�ĳ���ڵ��Ƿ�������д����������
    node: �ڵ�
    kv_map: ���Լ�����ֵ��ɵ�map'''
  for key in kv_map:
    if node.get(key) != kv_map.get(key):
      return False
  return True

#---------------search -----
def find_nodes(tree, path):
  '''����ĳ��·��ƥ������нڵ�
    tree: xml��
    path: �ڵ�·��'''
  return tree.findall(path)

def get_node_by_keyvalue(nodelist, kv_map):
  '''�������Լ�����ֵ��λ���ϵĽڵ㣬���ؽڵ�
    nodelist: �ڵ��б�
    kv_map: ƥ�����Լ�����ֵmap'''
  result_nodes = []
  for node in nodelist:
    if if_match(node, kv_map):
      result_nodes.append(node)
  return result_nodes

#---------------change -----
def change_node_properties(nodelist, kv_map, is_delete=False):
  '''�޸�/���� /ɾ�� �ڵ�����Լ�����ֵ
    nodelist: �ڵ��б�
    kv_map:���Լ�����ֵmap'''
  for node in nodelist:
    for key in kv_map:
      if is_delete:
        if key in node.attrib:
          del node.attrib[key]
      else:
        node.set(key, kv_map.get(key))

def change_node_text(nodelist, text, is_add=False, is_delete=False):
  '''�ı�/����/ɾ��һ���ڵ���ı�
    nodelist:�ڵ��б�
    text : ���º���ı�'''
  for node in nodelist:
    if is_add:
      node.text += text
    elif is_delete:
      node.text = ""
    else:
      node.text = text

def create_node(tag, property_map, content):
  '''����һ���ڵ�
    tag:�ڵ��ǩ
    property_map:���Լ�����ֵmap
    content: �ڵ�պϱ�ǩ����ı�����
    return �½ڵ�'''
  element = Element(tag, property_map)
  element.text = content
  return element

def add_child_node(nodelist, element):
  '''��һ���ڵ�����ӽڵ�
    nodelist: �ڵ��б�
    element: �ӽڵ�'''
  for node in nodelist:
    node.append(element)

def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
  '''ͬ�����Լ�����ֵ��λһ���ڵ㣬��ɾ��֮
    nodelist: ���ڵ��б�
    tag:�ӽڵ��ǩ
    kv_map: ���Լ�����ֵ�б�'''
  for parent_node in nodelist:
    children = parent_node.getchildren()
    for child in children:
      if child.tag == tag and if_match(child, kv_map):
        parent_node.remove(child)

if __name__ == "__main__":

    get_size()
    exit(0)

    origin_xml_path = 'tmp/161112_131733_origin.xml'
    output_xml_path = time.strftime("tmp/%y%m%d_%H%M%S_output.xml")
    try:
        
        tree = ElementTree()
        tree.parse(origin_xml_path)
        
        del_parent_nodes = tree.find('channel')
        
        for node in del_parent_nodes.findall('item'):
            details_url = node.find('link').text
            print details_url
            del_parent_nodes.remove(node)
        
        tree.write(output_xml_path, encoding = "utf-8", xml_declaration = True)
            
    except Exception as e:
        print e
        
    exit(0)
    
    #1. ��ȡxml�ļ�
    tree = read_xml("./test.xml")

    #2. �����޸�
    #A. �ҵ����ڵ�
    nodes = find_nodes(tree, "processers/processer")
    #B. ͨ������׼ȷ��λ�ӽڵ�
    result_nodes = get_node_by_keyvalue(nodes, {"name":"BProcesser"})
    #C. �޸Ľڵ�����
    change_node_properties(result_nodes, {"age": "1"})
    #D. ɾ���ڵ�����
    change_node_properties(result_nodes, {"value":""}, True)

    #3. �ڵ��޸�
    #A.�½��ڵ�
    a = create_node("person", {"age":"15","money":"200000"}, "this is the firest content")
    #B.���뵽���ڵ�֮��
    add_child_node(result_nodes, a)

    #4. ɾ���ڵ�
    #��λ���ڵ�
    del_parent_nodes = find_nodes(tree, "processers/services/service")
    #׼ȷ��λ�ӽڵ㲢ɾ��֮
    target_del_node = del_node_by_tagkeyvalue(del_parent_nodes, "chain", {"sequency" : "chain1"})

    #5. �޸Ľڵ��ı�
    #��λ�ڵ�
    text_nodes = get_node_by_keyvalue(find_nodes(tree, "processers/services/service/chain"), {"sequency":"chain3"})
    change_node_text(text_nodes, "new text")

    #6. ���������ļ�
    write_xml(tree, "./out.xml")