#!/bin/bash

function installOpera {
  step=$1
  echo $step
  while [ 1 -lt 5 ]
  do
       read   choose_value
       case "$choose_value" in
          Y )
              echo "`$2`"
              return
              ;;
          y  )
              echo "`$2`"
              return
              ;;
          N  )
              return
              ;;
          n  )
              return
              ;;
          *)
             echo "you must choose one [Y/N]?"
              ;;
       esac
  done
}



installOpera  "step 1,install flex.x86_64,[Y/N]?"  'yum -y install flex.x86_64'
installOpera  "step 2,install bison.x86_64,[Y/N]?"  'yum -y install bison.x86_64'
installOpera  "step 3,install byacc.x86_64,[Y/N]?"  'yum -y install byacc.x86_64'
installOpera  "step 4,install python-devel.x86_64,[Y/N]?"  'yum -y install python-devel.x86_64'
sleep 2
cd lib
echo "`tar -xvf libpcap-1.7.4.tar.gz`"
sleep 2
cd libpcap-1.7.4
echo "`./configure && make install`"
cd ..
sleep 2
echo "`unzip pypcap-master.zip`"
sleep 2
cd  pypcap-master
echo "`python setup.py install`"
cd ..
sleep 2
echo "`unzip dpkt-master.zip`"
sleep 2
cd  dpkt-master
echo "`python setup.py install`"

echo   all install success!