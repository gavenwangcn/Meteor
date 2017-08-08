'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
import capture_log
from socket import * 
import struct

def wapper_data(dpkt_request,send_port=80):
    data={}
    headers=dpkt_request.headers
    data_headers={}
    uri=dpkt_request.uri
    data.setdefault("uri",uri)
    data.setdefault("port",send_port)
    method= dpkt_request.method
    data.setdefault("method",method)
    # add body
    if(cmp(method,"POST")==0):
        # add body
        get_body = dpkt_request.body
        if(get_body):
            data.setdefault("body",get_body)
    # add header    
    for key,value in headers.iteritems():
        if(cmp(key,'if-modified-since')==0):continue
        if(cmp(key,'if-none-match')==0):continue
        if(cmp(key,'upgrade-insecure-requests')==0):continue
        if(cmp(key,'origin')==0):continue
        if(cmp(key,'content-length')==0):continue
        if(cmp(key,'host')==0):continue
        if(cmp(key,'connection')==0):continue
        if(cmp(key,'keep-alive')==0):continue
        if(cmp(key,'referer')==0):continue
        if(cmp(key,'user-agent')==0):continue
        if(cmp(key,'accept-encoding')==0):continue
        if(cmp(key,'accept-language')==0):continue
        if(cmp(key,'accept-charset')==0):continue
        if(cmp(key,'accept')==0):continue
        if(cmp(key,'cache-control')==0):continue
        data_headers.setdefault(key,value)
    if(len(data_headers)>0): 
        data.setdefault("headers",data_headers)
    return data

def send_single_UDP(dpkt_request,port,copy_ip,copy_port):
    method= dpkt_request.method
    if(cmp(method,"GET")==0 or cmp(method,"POST")==0):
        data=wapper_data(dpkt_request,port)
        capture_log.log_info("send data %s" % str(data))
        addr=(copy_ip, copy_port)
        sock = socket(AF_INET, SOCK_DGRAM) # UDP
        sock.connect(addr)
        sock.send(str(data))
    else:
        capture_log.log_error("error method %s" % method)
        pass
    
def send_groupcast_UDP(dpkt_request,port,copy_port,local_ip,group='224.1.1.1',ttl=255): 
    method= dpkt_request.method
    if(cmp(method,"GET")==0 or cmp(method,"POST")==0):
        data=wapper_data(dpkt_request,copy_port)
        sock = socket(AF_INET, SOCK_DGRAM,IPPROTO_UDP)
        sock.bind((local_ip,port))
        # Set Time-to-live (optional)
        ttl_bin = struct.pack('@i', ttl)
        sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, ttl_bin)
        status = sock.setsockopt(IPPROTO_IP,IP_ADD_MEMBERSHIP,inet_aton(group) + inet_aton(local_ip))   
        sock.sendto(data, (group, port))
    else:        
        capture_log.log_error("error method %s" % method)
        pass
          
if __name__ == '__main__':
    pass