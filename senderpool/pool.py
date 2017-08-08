'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-

import urllib2 
import pool_log
import threadpool


wm = threadpool.WorkerManager(10)
in_flag=True

def wapper_data(data,resent_ip,count):
    uri=data['uri']
    data_headers=None
    if(data.has_key('headers')):
        data_headers=data['headers']
        pool_log.log_debug("request headers %s" % data_headers) 
    port=data["port"]
    url = "http://%s:%s%s" % (resent_ip,port,uri)
    pool_log.log_info("request url %s" % url)   
    request=None
    # add body
    if(cmp(data['method'], "GET") == 0):
        request = urllib2.Request(url)
    elif(cmp(data['method'], "POST") == 0):
        get_body = data['body']
        message= "request body %s" % get_body
        pool_log.log_debug(message)
        request = urllib2.Request(url,str(get_body))
    # add header 
    if(request and data_headers):   
        for key,value in data_headers.iteritems():
            request.add_header(key, value)
    return request       

def send_request(request):
    try:
        response=urllib2.urlopen(request) 
        code =response.getcode()
        pool_log.log_info("response code %s" % code)
        if(code==302):
            redirect_url = response.geturl()
            pool_log.log_info("redirect to %s" % redirect_url)
            redirect_request = urllib2.Request(redirect_url)
            response=urllib2.urlopen(redirect_request)
    except Exception,e:
        error_str= "send request exception ,%s" % e
        pool_log.log_error(error_str)

def start_pool_send(message):
    pool_log.log_info(message)
    wm.wait_for_complete()

def stop_in_pool(message):
    pool_log.log_info(message)
    in_flag=False
    
def pool_data(data,resent_ip,count):
    request =wapper_data(data,resent_ip,count)
    if(in_flag and request):
        for i in range(int(count)):
            wm.add_job(send_request, request)
    else:pass        

if __name__ == '__main__':
    pass
                