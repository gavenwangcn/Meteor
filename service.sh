#!/bin/bash
if [ $# -lt 1 ];
then
  echo "USAGE: $0 classname opts"
  exit 1
fi



BASE_DIR=$(dirname $0)

# Returns 0 if the process with PID $1 is running.
function checkProcessIsRunning {
   local pid="$1"
#   echo "check pid:$1"
   if test $( ps -ef |  grep $pid | grep python | wc -l ) -lt 1 ; then return 1; fi
   return 0;
}

# Returns 0 when the service is running and sets the variable $pid to the PID.
function getServicePID {
   if [ ! -f $PID_FILE ]; then return 1; fi
   pid="$(<$PID_FILE)"
   checkProcessIsRunning $pid || return 1
   return 0; }

function startServiceProcess {  
   touch $PID_FILE
   rm -rf  $current_absolute_path/nohup.log
   nohup   $KEY_WORDS >> $current_absolute_path/nohup.log 2>&1 & echo $! > $PID_FILE
   sleep 0.1
   pid="$(<$PID_FILE)"
#   echo $pid
   if checkProcessIsRunning $pid; then :; else
      echo "$SERVICE_NAME start failed, see $current_absolute_path/nohup.log."
      return 1
   fi
   return 0;
}

function stopServiceProcess {
   STOP_DATE=`date +%Y%m%d%H%M%S`
   kill $pid || return 1
  # echo “stop 。。。。。。”
   for ((i=0; i<10; i++)); do
      checkProcessIsRunning $pid
      if [ $? -ne 0 ]; then
         #echo "正在删除$PID_FILE"
         rm -f $PID_FILE
         return 0
         fi
      sleep 1
      done
   echo "\n$SERVICE_NAME did not terminate within 10 seconds, sending SIGKILL..."
   kill -s KILL $pid || return 1
   local killWaitTime=15
   for ((i=0; i<10; i++)); do
      checkProcessIsRunning $pid
      if [ $? -ne 0 ]; then
         rm -f $PID_FILE
         return 0
         fi
      sleep 1
      done
   echo "Error: $SERVICE_NAME could not be stopped within 10 + 10 seconds!"
   return 1;
}

function startService {
   getServicePID
   if [ $? -eq 0 ]; then echo "$SERVICE_NAME is already running"; RETVAL=0; return 0; fi
   echo -n "Starting $SERVICE_NAME..."
   startServiceProcess
   if [ $? -ne 0 ]; then RETVAL=1; echo "failed"; return 1; fi
   COUNT=0
   while [ $COUNT -lt 1 ]; do
    for (( i=0;  i<5;  i=i+1 )) do
        STR=`grep "has started" $current_absolute_path/nohup.log`
        if [ ! -z "$STR" ]; then
            echo "PID=$pid\n"
            echo "Server start OK in $i seconds."
            break;
        fi
	    echo -e ".\c"
	    sleep 1
	done
	break
    done
echo "OK!"

#echo "PID: $START_PIDS"
#   echo "started PID=$pid"
   RETVAL=0
   return 0;
}

function stopService {
   getServicePID
   if [ $? -ne 0 ]; then echo -n "$SERVICE_NAME is not running"; RETVAL=0; echo ""; return 0; fi
   echo "Stopping $SERVICE_NAME... "
   stopServiceProcess
   if [ $? -ne 0 ]; then RETVAL=1; echo "failed"; return 1; fi
   echo "stopped PID=$pid"
   RETVAL=0
   return 0;
}

function checkServiceStatus {
   echo -n "Checking for $SERVICE_NAME: "
   if getServicePID; then
	echo "running PID=$pid"
	RETVAL=0
   else
	echo "stopped"
	RETVAL=3
   fi
   return 0;
}

function main {
   RETVAL=0
   case "$1" in
      start)
         stopService && startService
         ;;
      stop)
         stopService
         ;;
      restart)
         stopService && startService
         ;;
      status)
         checkServiceStatus
         ;;
      *)
         echo "Usage: $0 {service.sh start|stop|restart|status   capture|copyserver|sender}"
         exit 1
         ;;
      esac
   exit $RETVAL
}

function preOpration {
  #get absolute path
  current_absolute_path=`pwd`
   case "$1" in
      capture )
          cd $current_absolute_path/capture 
          KEY_WORDS="python -u start_capture.py"
          SERVICE_NAME="capture"
          ;;
      copyserver  )
          cd $current_absolute_path/copyserver 
          KEY_WORDS="python -u start_copy.py"
          SERVICE_NAME="copyserver"
          ;;
      sender  )
          cd $current_absolute_path/sender
          KEY_WORDS="python -u start_sender.py"
          SERVICE_NAME="sender"
          ;;
      *)
         echo "Usage: $0 {service.sh start|stop|restart|status   capture|copyserver|sender}"
         exit 1
          ;;
   esac
   PID_FILE="$SERVICE_NAME.pid"
}
preOpration $2

main $1
cd $current_absolute_path
