'''
Created on 2015

@author: 14020107
'''
import urllib2 
import send_log
import send_filter


def send_request(request):
    try:
        response=urllib2.urlopen(request) 
        code =response.getcode()
        send_log.log_debug("response code %s" % code)
        if(code==302):
            redirect_url = response.geturl()
            send_log.log_info("redirect to %s" % redirect_url)
            redirect_request = urllib2.Request(redirect_url)
            response=urllib2.urlopen(redirect_request)
        #print code
    except Exception,e:
        error_str= "send request exception ,%s" % e
        send_log.log_error(error_str)
        pass
    
def wapper_httpsend(data,resent_ip,count):
    if(send_filter.filter(data)):
        uri=data['uri']
        data_headers=None
        if(data.has_key('headers')):
            data_headers=data['headers']
            send_log.log_debug("request headers %s" % data_headers) 
        port=data["port"]
        url = "http://%s:%s%s" % (resent_ip,port,uri)
        send_log.log_info("request url %s" % url)   
        request=None
        # add body
        if(cmp(data['method'], "GET") == 0):
            request = urllib2.Request(url)
        elif(cmp(data['method'], "POST") == 0):
            get_body = data['body']
            message= "request body %s" % get_body
            send_log.log_debug(message)
            request = urllib2.Request(url,str(get_body))
        # add header 
        if(request and data_headers):   
            for key,value in data_headers.iteritems():
                request.add_header(key, value)
        if(request): 
            for i in range(int(count)): 
                send_request(request)     
        
if __name__ == '__main__':
    pass