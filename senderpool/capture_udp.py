'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
import pcap
import dpkt
import pool_log
import pool
import pool_config
import threading
import time,sched
from datetime import datetime
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
                            pool_log.log_info("get data: %s" % udp_data.data)
                            data = eval(udp_data.data) 
                            pool.pool_data(data, resent_ip, count)   
                        except Exception,e: 
                                error_str ="Capture src_ip %s:local_ip %s:dst_ip %s:exception: %s" % (src_ip,local_ip,dst_ip,e)     
                                pool_log.log_error(error_str)

def time_start():
        strt_time =pool_config.getConfig('pool', 'start_time')
        now =time.strftime('%H:%M:%S',time.localtime(time.time()))
        start=datetime.strptime(now,'%H:%M:%S')
        end=datetime.strptime(strt_time,'%H:%M:%S')
        sec =(end-start).seconds
        time_start =time.time()+sec
        return time_start


def pre_pool():
        hour =pool_config.getConfig('pool', 'pool_hour')
        strt_sec=600
        if(int(hour)>0):
            strt_sec=int(hour)*60*60
        tc = threading.Timer(strt_sec,pool.stop_in_pool,("stop in pool data.",))
        tc.start()
        sc = sched.scheduler(time_start,time.sleep)
        sc.enter(5,1,pool.start_pool_send,("start send message from pool.",))
        sc.run()
        
def capture(nc,resent_ip,count=5,port=65533):
        try:
            pre_pool()
            
            local_ip=get_local_ip(nc)                                                 
            # eth1
            pc = pcap.pcap(name="%s" % nc) 
            # tcp port 80                                        
            pc.setfilter('udp port %d' % port) 
            for p_time, p_data in pc:
                main_pcap(p_time, p_data, local_ip, port,resent_ip,count)
        except Exception,e: 
               error_str ="Capture network %s:port %s:resent_ip %s:exception: %s" % (nc,port,resent_ip,e)  
               pool_log.log_error(error_str)                                                                                
            
if __name__ == '__main__':
    pass
