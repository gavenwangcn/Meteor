'''
Created on 2015

@author: 14020107
'''
import threading
import time,sched
import pool_config
from datetime import datetime
import pool
 
def event_func(msg):
    print "Current Time:",time.time(),'msg:',msg
   
def time_start():
    now = time.time()
    midnight = now - (now % 86400) + time.timezone
    return midnight

def test_sched():
    s = sched.scheduler(time_start,time.sleep)
    s.enter(100,2,event_func,("Small event.",))
    s.enter(1,1,event_func,("Big event.",))
    s.run()

def time_start_b():
        strt_time =pool_config.getConfig('pool', 'start_time')
        now =time.strftime('%H:%M:%S',time.localtime(time.time()))
        start=datetime.strptime(now,'%H:%M:%S')
        end=datetime.strptime(strt_time,'%H:%M:%S')
        sec =(end-start).seconds
        time_start =time.time()+sec
        return time_start 
 
        
def test_func(msg1,msg2):
    print "I'm test_func,",msg1,msg2        
def test_time():
    t = threading.Timer(5,test_func,("msg1","msg2"))
    t.start()
    
def pre_pool():
        hour =pool_config.getConfig('pool', 'pool_hour')
        strt_sec=600
        if(int(hour)>0):
            strt_sec=int(hour)*60*60
        #tc = threading.Timer(strt_sec,pool.stop_in_pool,("stop in pool data.",))
        #tc.start()
        print time_start_b
        sc = sched.scheduler(time_start_b,time.sleep)
        sc.enter(5,1,pool.start_pool_send,("start send message from pool.",))
        sc.run()    
            
if __name__ == '__main__':
    now = time.time()
    hour =60*60*10
    print now
    print time.timezone
    midnight = now + hour 
    print midnight
    print time.ctime()
    a = '12:13:50'
    b = '19:06:03'
    test =time.strftime('%H:%M:%S',time.localtime(time.time()))
    time_a = datetime.strptime(a,'%H:%M:%S')
    time_b = datetime.strptime(test,'%H:%M:%S')

    print test
    print (time_a-time_b).seconds
    
    star= time_start_b()
    t_star=time.strftime('%H:%M:%S',time.localtime(star))
    print star
    print t_star
    pre_pool()
    #test_sched()
    