'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
import re
import copy_log
import copy_config

def reg_match(pre, line):
        p = re.compile(pre)
        m = p.match(line)
        return m  

def filter(data):
    flag =True;
    uri =data['uri']
    base_uri = "^/.*$"
    if not filter_base_uri(base_uri, uri): 
        flag=False;
        copy_log.log_error("not match base uri %s" % uri)
    if not filter_uri(uri):
        flag=False;
        copy_log.log_error("not match uri %s" % uri)    
    return flag;

def filter_base_uri(reg,uri):
    if not reg_match(reg, uri):
        return False
    else:
        return True

def filter_uri(uri):
    reg_uri=copy_config.getConfig("filter", "uri")
    if not reg_uri:
        return True
    else:
        if not reg_match(reg_uri, uri):
            return False
        else:
            return True
  

if __name__ == '__main__':
    pass