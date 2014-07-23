#!/bin/bash

#Create repo
for path in $(find ./ -type d | grep 'x86_64\|i386\|noarch\|armhfp\|SRPMS'| sed 's/\/repodata//g' | uniq)
do
	if [ `echo $path | grep epel-5` ];then
		echo -e "\n\ncreaterepo -v -s $path";
		createrepo -s sha $path
	else
		echo -e "\n\ncreaterepo -v $path"
		createrepo $path	
	fi
done

#Package signing
find ./ -type f | grep '\.rpm' | grep -v 'epel-5' | xargs rpmsign --addsign
