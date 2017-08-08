'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
import re
import send_log
import send_config

def reg_match(pre, line):
        p = re.compile(pre)
        m = p.match(line)
        return m  

def filter(data):
    flag =True;
    uri =data['uri']
    if not filter_uri(uri):
        flag=False;
        send_log.log_error("not match uri %s" % uri)     
    return flag;

def filter_uri(uri):
    reg_uri=send_config.getConfig("filter", "uri")
    if not reg_uri:
        return True
    else:
        if not reg_match(reg_uri, uri):
            return False
        else:
            return True

if __name__ == '__main__':
    pass