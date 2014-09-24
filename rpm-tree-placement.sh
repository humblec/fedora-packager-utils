#!/bin/bash 

rel=$1
download_path="./temp"

if [ $# -lt 1 ];then
	echo -e "\nUsage: $0  <os distribution>"
	echo -e "\n$0  fc[19 20 21 22]\n"
	echo -e "\n$0  el[5 6 7]\n"
	exit 1
fi

if [ ! -d ./temp ];then 
	echo "./temp is not present in current working directory";
	echo "Please download all the rpms from koji and put it in ./temp"
	exit 1
fi

if echo $rel | grep -i "fc" >/dev/null 2>&1;then
	os_ver=`echo $rel | sed 's/fc//'`
	path="Fedora/fedora-$os_ver"
	echo "Creating $path at `pwd`"
	mkdir -p $path/{SRPMS,i386,x86_64,noarch}
	if [ "$rel" != "19" ];then
		mkdir -p $path/armhfp
	fi
elif echo $rel | grep -i "el" >/dev/null 2>&1;then
	os_ver=`echo $rel | sed 's/el//'`
	path="EPEL.repo/epel-$os_ver"
	echo "Creating $path at `pwd`"
	mkdir -p $path/{SRPMS,i386,x86_64}
	if [ "$rel" != "5" ];then
		mkdir -p $path/noarch
	fi
fi

#
pwdir=`pwd`
cd ${download_path}

#delete duplicate rpms
for rpm in $(find ./ -type f)
do
	if echo $rpm | grep 'rpm\.'>/dev/null 2>&1;then
		rm -rf $rpm
	fi	
done
 
echo -e "\nListing RPMs\n"
ls

for rpm in $(find ./ -type f | grep "$rel" | grep 'x86_64\.rpm'); do mv $rpm ../$path/x86_64/;done
for rpm in $(find ./ -type f | grep "$rel" | grep 'src\.rpm'); do mv $rpm ../$path/SRPMS/;done

echo -e "\nChecking for i686 or i386  RPMs\n"
ls -l | grep 'i686\.rpm\|i386\.rpm'
if [ $? -eq '0' ];then
	echo -e "\ni686 or i386 RPMs are present"
	for rpm in $(find ./ -type f | grep "$rel" | grep 'i686\|i386'); do mv $rpm ../$path/i386/;done
fi

echo -e "\nChecking for noarch RPMs\n"
ls -l | grep 'noarch\.rpm'
if [ $? -eq '0' ];then
	echo -e "\nNoarch rpms are present"
	for rpm in $(find ./ -type f | grep "$rel" | grep 'noarch\.rpm'); do mv $rpm ../$path/noarch/;done
fi

echo -e "\nChecking for ARM RPMs\n"
ls -l | grep 'armv7hl\.rpm'
if [ $? -eq '0' ];then
	echo -e "\nARM rpms are present"
	for rpm in $(find ./ -type f | grep "$rel" | grep 'armv7hl\.rpm'); do mv $rpm ../$path/armhfp/;done
fi

tree ../$path

