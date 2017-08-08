'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
from socket import * 
import struct
import time
import copy_config
import copy_filter

def send_brocast_UDP(data,port,ttl=255):
    time.sleep(0.001)
    ips=copy_config.getConfig('config', 'ip')
    if(ips):
        ip_list =ips.split(',')
        send_single_ips(data,port,ip_list) 
    else:    
        host = '<broadcast>'
        addr = (host, port)
        sock = socket(AF_INET, SOCK_DGRAM)  
        sock.bind(('', 0))  #brocast
        ttl_bin = struct.pack('@i', ttl)
        sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, ttl_bin)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #brocast
        sock.sendto(data,addr)
    
def send_groupcast_UDP(data,port,local_ip,group='224.1.1.1',ttl=255): 
    if(copy_filter.filter(data)):
        time.sleep(0.001)
        ips=copy_config.getConfig('config', 'ip')
        if(ips):
            ip_list =ips.split(',')
            send_single_ips(data,port,ip_list)
        else:    
            sock = socket(AF_INET, SOCK_DGRAM,IPPROTO_UDP)
            sock.bind((local_ip,port))
            # Set Time-to-live (optional)
            ttl_bin = struct.pack('@i', ttl)
            sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, ttl_bin)
            status = sock.setsockopt(IPPROTO_IP,
                                     IP_ADD_MEMBERSHIP,
                                     inet_aton(group) + inet_aton(local_ip))   
            sock.sendto(data, (group, port))
    else:pass
def send_single_ips(data,port,ips):
    for ip in ips:
        addr=(ip, port)
        sock = socket(AF_INET, SOCK_DGRAM) # UDP
        sock.connect(addr)
        sock.send(str(data))
 
if __name__ == '__main__':
    pass