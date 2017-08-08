'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-
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
    
if __name__ == '__main__':
    pass
