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


# This program is a helper for gluster fedora package maintanance tasks.
# Using this program # you can pull the packages from koji and do package
# arrangements based on version/release  of the build.
# This program is  also capable of listing the packages in a directory
# and verifying its integrity
#



import os
import glob
import subprocess
import sys
from optparse import OptionParser
from rpmUtils.miscutils import splitFilename



def verify_rpms(destdir, packages, pkgcount):

    """
     Function to verify the files are real RPMS
    :param destdir: the directory in which RPMs are stored.
    :param packages: the package list
    :param pkgcount: the number of packages in the destdir
    :return:
    """
    count=0
    for i in packages:
        p1 = subprocess.Popen(['file',i] , stdout= subprocess.PIPE)
        out = p1.communicate()[0]
        if 'RPM' in out:
            print "\t \t ---->  Verified : RPM package"
            count = count+1
        else:
            print "\t \t \t  ---->   I found a NON RPM package !!!"
    if count == pkgcount:
        if pkgcount != 0 :
            print " \t \t \t \t All the packages are valid RPMs "
        else:
            print "--------------   WARNING : No Packages exist in this dir %s--------------" % (destdir)
    else:
        print " \n \t \t \tCRITICAL ERROR ******** I failed to verify all the RPMs in the directory %s" % (destdir)
    return True


def list_rpms(sourcedir):

    """
    :param sourcedir: the directory to list rpms
    :return:
    """
    number = 0
    orig_path=sourcedir+'/'+'*.rpm'
    pack_list = glob.glob(orig_path)
    for pck in pack_list:
        number +=1
        print pck
    if number != 0:
        print "\t \t %s packages exist in this dir" %(number)
    verify_rpms(sourcedir,pack_list, number)
    return True


def post_spread(where):

    """
    :param: where:  The directory where Fedora and EPEL directories are created.
    """

    fedora_base = where+'/'+"Fedora"
    epel_base = where+"/"+"EPEL"
    if not os.path.exists(fedora_base):
        os.makedirs(fedora_base)
    if not os.path.exists(epel_base):
        os.makedirs(epel_base)

    for dirs in os.listdir(where):
        cmd = "--backup --suffix \"-`date +\"%F-%T\"`\""
        if "fc" in dirs:
            print "Fedora:%s" %(dirs)
            os.system("mv"+ " "+"fc*"+" "+fedora_base+" "+cmd)
        if "el" in dirs:
            print "EPEL:%s" %(dirs)
            os.system("mv"+ " "+"el*"+" "+epel_base+" "+cmd)
    return True

def tree_it (which_dir):

    """
    :param which_dir: The directory on which tree command should be executed
    :return:
    """

    os.system("tree"+" "+which_dir)
    rootDir = which_dir
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('\n \t \t Directory: %s \n' % dirName)
        list_rpms(dirName)
        #for fname in fileList:
        #    print('\t%s' % fname)

    return True

def spread_packages (sourcedir, destdir):

    """
    :param sourcedir: The directory on which all the downloaded rpms are stored.
    :param destdir  : The directory in which the packages will  be kept based on fedora and epel version
    :return:
    """

    number = 0
    orig_path=sourcedir+'/'+'*.rpm'
    pack_list = glob.glob(orig_path)
    for pck in pack_list:
        number +=1
        (n, v, r, e, a) = splitFilename(pck)
        distribution =  r.split('.')[-1]
        # validating whether its an fedora/epel rpm.
        if "fc" in distribution:
            print "\t Fedora rpm   --> %s %s %s %s %s" %(n, v, r, e, a)
        if 'el' in distribution:
            print "\t EPEL package --> %s %s %s %s %s" %(n, v, r, e, a)


        try:
            if not os.path.exists(destdir+'/'+distribution+'/'+a):
                os.makedirs(destdir+'/'+distribution+'/'+a)
            source_file = pck
            if "gluster" in pck:
                destination_file = destdir+'/'+distribution+'/'+a
                os.system("cp"+" " +source_file+" "+destination_file)
            else:
                print "Not a Gluster RPM :%s" %(pck)
        except:
            raise

    post_spread(destdir)
    print " *******  LISTING PACKAGES FOR U!! ********"
    tree_it(destdir)
    return True




def pull_packages(sourcedir):
    """

    :param sourcedir: The directory where the pulled rpms are stored
    :return:
    Additional Info: pulling packages are really tricky. It is not 100% sure shot currently. Because of the
    taskids koji trigger for different builds. However we manage to pull almost all rpms via couple of different
    iterations. The other option in just pulling by 1 taskid at a time, it works well.
    """
    """
    :param sourcedir:
    :return:
    """
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
        ret = os.system(pullcmd)
        if ret:

            print "Error occurred.. please check and rerun if required"
        else:
            print " \t Successfully downloaded.. Verify downloaded RPMS"



def main():

    parser = OptionParser()
    parser.add_option("-p", "--pull",
                      action="store_true", dest="pull", default=False,
                      help="Pull packages from koji repo based on the taskid?")


    parser.add_option("-s", "--spread",
                      action="store_true", dest="spread", default=False,
                      help="Spread fedora and EPEL rpms from specified directory to approprite arch and distro")


    options, arguments = parser.parse_args()

    anyopt = [ options.pull , options.spread]
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
        source_spread_dir = raw_input("Enter the source directory where the rpms are stored.:")
   
        dest_spread_dir = raw_input("Enter the destination directory where the rpms are stored.:")

        spread_packages(source_spread_dir, dest_spread_dir)


if __name__ == '__main__':
    #print "Starting %s ......." % (__name__)
    main()
