#!/bin/bash

path=$1
cd $path
if [ $? -ne 0 ];then
    echo -e "\n$path is not valid"
    exit 1
fi

mkdir x86_64
for rpm in $(find ./ -type f | grep 'x86_64\.rpm'); do mv $rpm $path/x86_64/;done

mkdir SRPMS
for rpm in $(find ./ -type f | grep 'src\.rpm'); do mv $rpm $path/SRPMS/;done

echo -e "\nChecking for i686 or i386  RPMs\n"
ls -l | grep 'i686\.rpm\|i386\.rpm'
if [ $? -eq '0' ];then
	echo -e "\ni686 or i386 RPMs are present"
    mkdir i386
	for rpm in $(find ./ -type f | grep 'i686\.rpm'); do mv $rpm $path/i386/;done
fi

echo -e "\nChecking for noarch RPMs\n"
ls -l | grep 'noarch\.rpm'
if [ $? -eq '0' ];then
	echo -e "\nNoarch rpms are present"
    mkdir noarch
	for rpm in $(find ./ -type f | grep 'noarch\.rpm'); do mv $rpm $path/noarch/;done
fi

echo -e "\nChecking for ARM RPMs\n"
ls -l | grep 'armv7hl\.rpm'
if [ $? -eq '0' ];then
	echo -e "\nARM rpms are present"
    mkdir armhfp
	for rpm in $(find ./ -type f | grep 'armv7hl\.rpm'); do mv $rpm $path/armhfp/;done
fi

tree $path
