'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
import sys
import pcap
import dpkt
import capture_filter
import capture_log
import capture_send
import capture_config
import socket, fcntl, struct 



def get_local_ip(ifname):  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
    ret = socket.inet_ntoa(inet[20:24])  
    return ret

def exclude_ip(src_ip,exclude_ips):
    flag =True
    if(exclude_ips):
        exclude_ips=exclude_ip.split(',')
        for exclude in exclude_ips:
            if(cmp(src_ip, exclude) == 0):
                  flag=False     
    return flag
       
def main_pcap(p_time, p_data, local_ip, port, copy_ip, copy_port,exclude_ips):  
        p = dpkt.ethernet.Ethernet(p_data)                                      
        if p.data.__class__.__name__ == 'IP':
                ip_data = p.data
                src_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_data.src)))
                if(cmp(src_ip, local_ip) != 0 and exclude_ip(src_ip,exclude_ips)):
                    if p.data.data.__class__.__name__=='TCP':
                            tcp_data = p.data.data
                            if tcp_data.dport==port:
                                    if tcp_data.data:
                                        try:
                                            dpkt_request = dpkt.http.Request(tcp_data.data) 
                                            # src send packet not capture
                                            capture_send.send_single_UDP(dpkt_request,port,copy_ip,copy_port)   
                                        except Exception,e: 
                                            error_str ="Capture src_ip %s:local_ip %s:exception: %s" % (src_ip,local_ip,e)  
                                            capture_log.log_error(error_str)
                                            pass   

def capture(nc,port,copy_ip,copy_port=65533):
        try:
            local_ip=get_local_ip(nc)
            exclude_ips = capture_config.getConfig("exclude", 'ip')                                                 
            # eth1
            pc = pcap.pcap(name="%s" % nc) 
            # tcp port 80                                        
            pc.setfilter('tcp port %d' % port) 
            for p_time, p_data in pc:
                main_pcap(p_time, p_data, local_ip, port, copy_ip, copy_port,exclude_ips)
        except Exception,e: 
               error_str ="Capture network %s:port %s:copy_ip %s: copy_port %s:exception: %s" % (nc,port,copy_ip,copy_port,e)  
               print error_str
               sys.exit(1)                                                                                   
            
if __name__ == '__main__':
    pass
