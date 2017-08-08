'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
import re
import capture_log
import capture_config

def reg_match(pre, line):
        p = re.compile(pre)
        m = p.match(line)
        return m  

def filter(dpkt_request):
    flag =True;
    uri =dpkt_request.uri
    host =None
    http_headers = dpkt_request.headers
    if(http_headers.has_key('host')):
        host = http_headers['host']
    if not filter_uri(uri):
        flag=False;
        capture_log.log_error("not match uri %s" % uri)
    if host:    
        if not filter_host(host):
            flag=False;
            capture_log.log_error("not match host %s" % host)      
    return flag;

def filter_uri(uri):
    reg_uri=capture_config.getConfig("filter", "uri")
    if not reg_uri:
        return True
    else:
        if not reg_match(reg_uri, uri):
            return False
        else:
            return True

def filter_host(host):
    reg_host=capture_config.getConfig("filter", "host")
    if not host:
        return True
    else:
        if not reg_match(reg_host, host):
            return False
        else:
            return True    
  

if __name__ == '__main__':
    pass