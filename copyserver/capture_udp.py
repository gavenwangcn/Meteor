'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
import sys
import pcap
import dpkt
import copy_log
import copy_udp
import socket, fcntl, struct 

def get_local_ip(ifname):  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
    ret = socket.inet_ntoa(inet[20:24])  
    return ret                       
           
def main_pcap(p_time,p_data,local_ip,port):  
        p = dpkt.ethernet.Ethernet(p_data)                                      
        if p.type == dpkt.ethernet.ETH_TYPE_IP:
                ip_data = p.data
                src_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_data.src)))
                if ip_data.p == dpkt.ip.IP_PROTO_UDP:
                    udp_data = p.data.data
                    if(cmp(src_ip, local_ip) != 0):
                            if udp_data.data:
                                try:
                                    copy_log.log_info("send copy data: %s" % udp_data.data)
                                    copy_udp.send_groupcast_UDP(udp_data.data,port,local_ip)  
                                except Exception,e: 
                                            error_str ="Capture src_ip %s:local_ip %s:exception: %s" % (src_ip,local_ip,e)  
                                            copy_log.log_error(error_str)
                                            pass   

def capture(nc,port=65533):
        try:
            local_ip=get_local_ip(nc)                                                 
            # eth1
            pc = pcap.pcap(name="%s" % nc) 
            # tcp port 80                                        
            pc.setfilter('udp port %d' % port) 
            for p_time, p_data in pc:
                main_pcap(p_time, p_data, local_ip, port)
        except Exception,e: 
               error_str ="Copy network %s:port %s:exception: %s" % (nc,port,e)  
               copy_log.log_error(error_str)
               sys.exit(1)
               pass                                                                                   
           
if __name__ == '__main__':
    pass
