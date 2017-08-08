'''
@author: 14020107
'''
# -*- coding: utf-8 -*-
import sys
import capture
import capture_config
import capture_log

def start():
    
    if(len(sys.argv)<4):
        capture_nc=capture_config.getConfig("config", 'nc')
        if(not capture_nc):
            print "error not have network card info"
            capture_log.log_error("error not have network card info")
            sys.exit(1)
        capture_port=capture_config.getConfig("config", 'capture_port')
        if(not capture_port):
            print "error not have capture port info"
            capture_log.log_error("error not have capture port info")
            sys.exit(1)
        copy_ip=capture_config.getConfig("config", 'copy_ip')
        if(not copy_ip):    
            print "error not have copyserver ip info"
            capture_log.log_error("error not have copyserver ip info")
            sys.exit(1)
        print"Start capture port: %s network card: %s copy ip: %s" % (capture_port,capture_nc,copy_ip)
        capture_log.log_info("Start capture port: %s network card: %s copy ip: %s" % (capture_port,capture_nc,copy_ip))
        copy_port=capture_config.getConfig("config", 'copy_port')
        if(copy_port):
            capture.capture(capture_nc, int(capture_port),copy_ip,int(copy_port));
        else:            
            capture.capture(capture_nc, int(capture_port),copy_ip);    
    else:
       capture_nc =sys.argv[1]
       capture_port=int(sys.argv[2])
       copy_ip=sys.argv[3]
       print"Start capture port: %s network card: %s copy ip: %s" % (capture_port,capture_nc,copy_ip)
       if(len(sys.argv)==5):
           copy_port=sys.argv[4]
           capture.capture(capture_nc, capture_port,copy_ip,copy_port);
       else:   
           capture.capture(capture_nc, capture_port,copy_ip);
       
if __name__ == '__main__':
    start() 
          