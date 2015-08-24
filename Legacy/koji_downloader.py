#!/usr/bin/python

# Copyright (C) 2014 Red Hat Inc.
# Author Humble Chirammal <humble.devassy@gmail.com> | <hchiramm@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import glob
import subprocess
import sys
from optparse import OptionParser

def verify_rpms(destdir, packages):
    for i in packages:
        p1 = subprocess.Popen(['file',i] , stdout= subprocess.PIPE)
        out = p1.communicate()[0]
        print out
        if 'RPM' in out:
            print "\t \t ---->  Verified : RPM package"
        else:
            print "\t \t \t  ---->   I found a NON RPM package !!!"



def list_rpms(sourcedir):
    number = 0
    orig_path=sourcedir+'/'+'*.rpm'
    pack_list = glob.glob(orig_path)
    for pck in pack_list:
        number +=1
        print pck
    print "\t \t %s packages exist in this dir" %(number)
    verify_rpms(sourcedir,pack_list)




def pull_packages(sourcedir):
    os.chdir(sourcedir)
    task_id = raw_input ("Enter path for taskid (ex:7034519):")
    count = int(raw_input("no of architectures:"))

    for i in range(0,count):
        parent_dir = task_id[-4:]
        task_id_int=int(task_id)+1
        parent_dir_int=int(parent_dir)+1
        task_id= str(task_id_int)
        parent_dir=str(parent_dir_int)
        pullcmd = 'wget -e robots=off --cut-dirs=4 --user-agent=Mozilla/5.0 --reject="index.html*" --reject="*.log" ' \
              '--no-parent --recursive --relative --level=1 --no-directories ' \
              'https://kojipkgs.fedoraproject.org//work/tasks/'+parent_dir+'/'+task_id+'/'
        print pullcmd
        ret = os.system(pullcmd)
        if ret:

            print "Error occurred.. please check and rerun if required"
        else:
            print " \t Successfully downloaded.. Verify downloaded RPMS"



def main():
    flag = 0
    parser = OptionParser()
    parser.add_option("-p", "--pull",
                      action="store_true", dest="pull", default=False,
                      help="Pull packages from koji repo based on the taskid?")

    parser.add_option("-l", "--list",
                      action="store_true", dest="list", default=False,
                      help="List packages in specified directory")

    parser.add_option("-v", "--verify",
                      action="store_true", dest="verify", default=False,
                      help="Verify  packages in specified directory")

    options, arguments = parser.parse_args()
    anyopt = [ options.pull , options.list , options.verify]
    check = [o for o in anyopt if o]
    if not check:
        print  "You missed one of the must required option.. reread and execute.... exiting ."
        parser.print_help()

        sys.exit(1)
    if options.pull:
        print "action: pull"
        pull_dir = raw_input("Enter the directory path to pull packages :")
        pull_packages(pull_dir)

    if options.list or options.verify:
            if flag == 0:
                print 'action: list/verify'
                list_dir = raw_input("Enter the directory path to list/verify packages :")
                flag =1
                list_rpms(list_dir)


if __name__ == '__main__':
    #print "Starting %s ......." % (__name__)
    main()