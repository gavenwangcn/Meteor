'''
Created on 2015

@author: 14020107
'''
import capture_config

exclude_ip = capture_config.getConfig("exclude", 'ip')

def exclude_ip(src_ip):
    flag =True
    if(exclude_ip):
        exclude_ips=exclude_ip.split(',')
        for exclude in exclude_ips:
            if(cmp(src_ip, exclude) == 0):
                  flag=False     
    return flag

if __name__ == '__main__':
        #start() 
    capture_nc=capture_config.getConfig("config", 'nc')
    copy_ip=capture_config.getConfig("config", 'copy_ip')
    print "capture_nc %s " % capture_nc
    if(not copy_ip):
        print "copy_ip %s " % copy_ip
        
    print exclude_ip('192.168.1.3')    
        
       