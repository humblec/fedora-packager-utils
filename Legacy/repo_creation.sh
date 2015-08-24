#!/bin/bash
#Run as root
#Create repo
repo_path=$1
if [ $# -lt 1 ];then
        echo -e "\n$0 <path>"
        echo -e "\n$0 /home/glusterpackager/repo-352-1\n"
        exit 1
fi

if ! `whoami | grep root >/dev/null 2>&1`;then
	echo "Please run the script as root"
	exit 1
fi

for path in $(find ${repo_path} -type d | grep 'x86_64\|i386\|noarch\|armhfp\|SRPMS'| sed 's/\/repodata//g' | uniq)
do
	if [ `echo $path | grep epel-5` ];then
		echo -e "\n\ncreaterepo -v -s $path";
		createrepo -s sha $path
	else
		echo -e "\n\ncreaterepo -v $path"
		createrepo $path	
	fi
done

#Check the rpm numbers in each dir
echo -e "\nCheck the rpm numbers in each dir\n"
for path in $(find ${repo_path} -type d | sed 's/\/repodata//g'|uniq | grep 'x86_64\|i386\|SRPMS\|noarch')
do 
	echo $path;ls -l $path | grep -v 'total\|repodata' | wc -l;
	sleep 1;
done

