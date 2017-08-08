'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
import pcap
import dpkt
import send_log
import httpsend
import socket, fcntl, struct 

def get_local_ip(ifname):  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
    ret = socket.inet_ntoa(inet[20:24])  
    return ret                       
           
def main_pcap(p_time,p_data,local_ip,port,resent_ip,count):  
        p = dpkt.ethernet.Ethernet(p_data)                                      
        if p.type == dpkt.ethernet.ETH_TYPE_IP:
                ip_data = p.data
                src_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_data.src)))
                dst_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_data.dst)))
                if ip_data.p == dpkt.ip.IP_PROTO_UDP:
                    udp_data = p.data.data
                    if udp_data.data:
                        try:
                            send_log.log_info("get data: %s" % udp_data.data)
                            data = eval(udp_data.data) 
                            httpsend.wapper_httpsend(data,resent_ip,count)   
                        except Exception,e: 
                                error_str ="Capture src_ip %s:local_ip %s:dst_ip %s:exception: %s" % (src_ip,local_ip,dst_ip,e)  
                                send_log.log_error(error_str)
                                pass   

def capture(nc,resent_ip,count=5,port=65533):
        try:
            local_ip=get_local_ip(nc)                                                 
            # eth1
            pc = pcap.pcap(name="%s" % nc) 
            # tcp port 80                                        
            pc.setfilter('udp port %d' % port) 
            for p_time, p_data in pc:
                main_pcap(p_time, p_data, local_ip, port,resent_ip,count)
        except Exception,e: 
               error_str ="Capture network %s:port %s:resent_ip %s:exception: %s" % (nc,port,resent_ip,e)  
               print error_str
               pass                                                                                   
            
if __name__ == '__main__':
    pass
