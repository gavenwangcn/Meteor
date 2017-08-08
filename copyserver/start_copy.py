'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
import sys
import capture_udp
import copy_config
import copy_log

def start():
    if(len(sys.argv)<2):
        capture_nc=copy_config.getConfig("config", 'nc')
        port =copy_config.getConfig("config", 'port')
        if(capture_nc):
            print"Start copysever network card: %s" % (capture_nc)
            copy_log.log_info("Start copysever network card: %s" % (capture_nc))
            if(port):
                capture_udp.capture(capture_nc,int(port));
            else:
                capture_udp.capture(capture_nc); 
        else:
            print "error not have network card info"
            copy_log.error_log("error not have network card info")
            sys.exit(1)
    else:
       capture_nc =sys.argv[1]
       print"Start copysever network card: %s" % (capture_nc)
       if(len(sys.argv)==3):
           port=sys.argv[2]
           capture_udp.capture(capture_nc,port);
       else:   
           capture_udp.capture(capture_nc);
       
if __name__ == '__main__':
    start()       
       
          