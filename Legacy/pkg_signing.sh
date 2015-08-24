#!/bin/bash
path=$1
if [ $# -lt 1 ];then
        echo -e "\n$0 <path>"
        echo -e "\n$0 /home/glusterpackager/repo-352-1\n"
        exit 1
fi

#Package signing
#Run as gluster packager
find ${path} -type f | grep '\.rpm' | grep -v 'epel-5' | xargs rpmsign --addsign

