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
from rpmUtils.miscutils import splitFilename



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

def post_spread(where):

    fedora_base = where+'/'+"Fedora"
    epel_base = where+"/"+"EPEL"
    if not os.path.exists(fedora_base):
        os.makedirs(fedora_base)
    if not os.path.exists(epel_base):
        os.makedirs(epel_base)

    for dirs in os.listdir(where):
        #print dirs
        cmd = "--backup --suffix \"-`date +\"%F-%T\"`\""
        if "fc" in dirs:
            print "Fedora:%s" %(dirs)
            os.system("mv"+ " "+"fc*"+" "+fedora_base+" "+cmd)
        if "el" in dirs:
            print "EPEL:%s" %(dirs)
            os.system("mv"+ " "+"el*"+" "+epel_base+" "+cmd)

def tree_it (which_dir):

    os.system("tree"+" "+which_dir)

def spread_packages (sourcedir, destdir):
    number = 0
    orig_path=sourcedir+'/'+'*.rpm'
    pack_list = glob.glob(orig_path)
    for pck in pack_list:
        number +=1
       # print pck
        (n, v, r, e, a) = splitFilename(pck)
        #print (n, v, r, e, a)
        distribution =  r.split('.')[-1]
        if "fc" in distribution:
            print "Fedora rpm --> %s %s %s %s %s" %(n, v, r, e, a)
        if 'el' in distribution:
            print "EPEL package --> %s %s %s %s %s" %(n, v, r, e, a)


        try:
            if not os.path.exists(destdir+'/'+distribution+'/'+a):
                os.makedirs(destdir+'/'+distribution+'/'+a)
            source_file = pck
            destination_file = destdir+'/'+distribution+'/'+a
            #print source_file
            #print destination_file
            os.system("cp"+" " +source_file+" "+destination_file)

            # Now keep fc folders in Fedora and 'el' folders in EPEL

        except:
            raise

    post_spread(destdir)

#TODO : Make automatic verification of rpms here.

    print " ******* VERIFY YOURSELF... I AM LISTING PACKAGES FOR U!! ********"
    #print destdir
    tree_it(destdir)
    print "\t \t %s packages exist in this dir" %(number)




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
        #print pullcmd
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

    parser.add_option("-s", "--spread",
                      action="store_true", dest="spread", default=False,
                      help="Spread fedora and EPEL rpms from specified directory to approprite arch and distro")

    parser.add_option("-v", "--verify",
                      action="store_true", dest="verify", default=False,
                      help="Verify  packages in specified directory")

    options, arguments = parser.parse_args()
    anyopt = [ options.pull , options.spread, options.list , options.verify]
    check = [o for o in anyopt if o]
    if not check:
        print  "You missed one of the must required option.. reread and execute.... exiting ."
        parser.print_help()

        sys.exit(1)
    if options.pull:
        print "action: pull"
        pull_dir = raw_input("Enter the directory path to pull packages :")
        pull_packages(pull_dir)

    if options.spread:
        print "action: spread"
        #source_spread_dir = raw_input("Enter the source directory where the rpms are stored.:")
        source_spread_dir='/home/hchiramm/gluster_package_backup'
        #dest_spread_dir = raw_input("Enter the destination directory where the rpms are stored.:")
        dest_spread_dir='./'
        spread_packages(source_spread_dir, dest_spread_dir)


    if options.list or options.verify:
            if flag == 0:
                print 'action: list/verify'
                list_dir = raw_input("Enter the directory path to list/verify packages :")
                flag =1
                list_rpms(list_dir)


if __name__ == '__main__':
    #print "Starting %s ......." % (__name__)
    main()