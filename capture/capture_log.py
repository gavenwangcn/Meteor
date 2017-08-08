'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
import datetime
import logging.config

logging.config.fileConfig("logger.conf")
console_log = logging.getLogger("console")
info_log = logging.getLogger("info")
error_log = logging.getLogger("error")

def console(message):
    console_log.debug(message)
    
def log_debug(message):
    info_log.debug(message) 

def log_warn(message):
    info_log.warn(message)     

def log_info(message):
    info_log.info(message)  
    
def log_error(e):    
    error_log.error(e)


def log(p_time,src_ip,dst_ip,dpkt_request):
    out_format = "%s\t%s\t%s\t%s\t%s\tHTTP/%s\t%s\t%s"
    ret = out_format % (str(datetime.datetime.utcfromtimestamp(p_time)), src_ip, dst_ip, dpkt_request.method, dpkt_request.uri, dpkt_request.version, dpkt_request.body, dpkt_request.headers)
    info_log.info(ret)
    
if __name__ == '__main__':
        pass
