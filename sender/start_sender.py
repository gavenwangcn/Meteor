'''
@author: 14020107
'''
# -*- coding: utf-8 -*-
import sys
import capture_udp
import send_config
import send_log

def start():
    if(len(sys.argv)<3):
        capture_nc=send_config.getConfig("config", 'nc')
        if(not capture_nc):
            print "error not have network card info"
            send_log.log_error("error not have network card info")
            sys.exit(1)
        resent_ip=send_config.getConfig("config", 'resent_ip')
        if(not resent_ip):
            print "error not have resent ip info"
            send_log.log_error("error not have resent ip info")
            sys.exit(1)
        print"Start sender sever network card: %s resent ip: %s" % (capture_nc,resent_ip)
        send_log.log_info("Start sender sever network card: %s resent ip: %s" % (capture_nc,resent_ip))
        count=send_config.getConfig("config", 'count')
        port=send_config.getConfig("config", 'port')
        if(count):
            if(port):
                capture_udp.capture(capture_nc, resent_ip,count,int(port));
            else:
                capture_udp.capture(capture_nc,resent_ip,count);
        else:            
            capture_udp.capture(capture_nc, resent_ip);
    else:
       capture_nc =sys.argv[1]
       resent_ip=sys.argv[2]
       print"Start sender sever network card: %s resent ip: %s" % (capture_nc,resent_ip)
       if(len(sys.argv)==4):
           count=sys.argv[3]
           capture_udp.capture(capture_nc,resent_ip,count);
       elif(len(sys.argv)==5): 
           count=sys.argv[3]   
           port=sys.argv[4]
           capture_udp.capture(capture_nc, resent_ip,count,port);
       else:   
           capture_udp.capture(capture_nc, resent_ip);
       
if __name__ == '__main__':
    start()       
       
          