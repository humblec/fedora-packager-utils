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


fedora_dirs = ['fedora-19', 'fedora-20', 'fedora-21','fedora-22','fedora-23','fedora-24']
epel_dirs = ['epel-5','epel-6','epel-7']
fedoradir=''
epeldir=''

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

def repo_creation(fedoradir,epeldir):
    build_list =["x86_64","i386","i686","noarch","armhfp","armv7hl","ppc","ppc64","SRPMS"]
    os.system("cp /home/glusterpackager/glusterfs-epel.repo "+epeldir)
    os.system("cp /home/glusterpackager/glusterfs-epel.repo.el5 "+epeldir)
    os.system("cp /home/glusterpackager/pub.key "+epeldir)
    os.system("cp /home/glusterpackager/pub.key "+fedoradir)
    os.system("cp /home/glusterpackager/glusterfs-fedora.repo "+fedoradir)
    for dirs in os.listdir(epeldir):
        if dirs == "epel-5":
                epel5dirs=epeldir+"/"+dirs
                for e5dir in os.listdir(epel5dirs):
                    if e5dir in build_list:
                        print "\ncreaterepo -v -s "+epel5dirs+'/'+e5dir+"\n"
                        os.system("createrepo -s sha "+epel5dirs+'/'+e5dir)
        if dirs in ["epel-6","epel-7"]:
                edirs = epeldir+'/'+dirs
                for edir in os.listdir(edirs):
                    if edir in build_list:
                        print "\ncreaterepo -v "+edirs+'/'+edir+"\n"
                        os.system("createrepo "+edirs+'/'+edir)

    for dirs in os.listdir(fedoradir):
        if dirs in fedora_dirs:
                fdirs = fedoradir+'/'+dirs
                for fdir in os.listdir(fdirs):
                    if fdir in build_list:
                        print "\ncreaterepo -v "+fdirs+'/'+fdir+"\n"
                        os.system("createrepo "+fdirs+'/'+fdir)

    print "\nCheck the rpm numbers in each directorys"
    for dirs in os.listdir(epeldir):
        if dirs in epel_dirs:
                edirs = epeldir+'/'+dirs
                for edir in os.listdir(edirs):
                    if edir in build_list:
                        orig_path=edirs+'/'+edir+'/*.rpm'
                        print "\n"+edirs+'/'+edir
                        print len(glob.glob(orig_path))

    for dirs in os.listdir(fedoradir):
        if dirs in fedora_dirs:
                fdirs = fedoradir+'/'+dirs
                for fdir in os.listdir(fdirs):
                    if fdir in build_list:
                        orig_path=fdirs+'/'+fdir+'/*.rpm'
                        print "\n"+fdirs+'/'+fdir
                        print len(glob.glob(orig_path))
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

def rearrange_packages(source_rearrange_fedoradir, source_rearrange_epeldir):
    #os.chdir(source_rearrange_dir)
    #for dirs in os.listdir(source_rearrange_dir):
#	print dirs
#	if dirs == "EPEL.repo":
#		source_rearrange_epeldir = source_rearrange_dir+'/'+'EPEL.repo'
#	if dirs == "Fedora":
#		source_rearrange_fedoradir = source_rearrange_dir+'/'+'Fedora'
    os.chdir(source_rearrange_epeldir)
    for dirs in os.listdir(source_rearrange_epeldir):
	if dirs == "el5":
		os.system("mv"+" "+"el5"+" "+ "epel-5")
	if dirs == "el6":
		os.system("mv"+" "+"el6"+" "+ "epel-6")
	if dirs == "el7":
		os.system("mv"+" "+"el7"+" "+ "epel-7")
    os.chdir(source_rearrange_fedoradir)

    for dirs in os.listdir(source_rearrange_fedoradir):
	if dirs == "fc19":
		os.system("mv"+" "+"fc19"+" "+ "fedora-19")
	if dirs == "fc20":
		os.system("mv"+" "+"fc20"+" "+ "fedora-20")
	if dirs == "fc21":
		os.system("mv"+" "+"fc21"+" "+ "fedora-21")
	if dirs == "fc22":
		os.system("mv"+" "+"fc22"+" "+ "fedora-22")
	if dirs == "fc23":
		os.system("mv"+" "+"fc23"+" "+ "fedora-23")
	if dirs == "fc24":
		os.system("mv"+" "+"fc24"+" "+ "fedora-24")
	    print source_rearrange_fedoradir
    for i in fedora_dirs:
	os.system("mv"+" "+i+"/src"+" "+i+"/SRPMS")

    os.chdir(source_rearrange_epeldir)
    for i in epel_dirs:
	os.system("mv"+" "+i+"/src"+" "+i+"/SRPMS")

    fedoradir=source_rearrange_fedoradir
    epeldir=source_rearrange_epeldir
    rpm_signing(fedoradir,epeldir)
    return True

def rpm_signing(fedoradir, epeldir):
    os.chdir(fedoradir)
    os.system("rpmsign"+" "+"--addsign"+" "+"*/*/*.rpm")
    print "Fedora RPMS signed properly"
    os.chdir(epeldir)
    os.system("rpmsign"+" "+"--addsign"+" "+"epel-[67]/*/*.rpm")
    print "EPEL RPMS signed properly"

def link_creation(fedoradir, epeldir):
    os.chdir(epeldir)
    for k in epel_dirs:
	if k == "epel-5":
		os.system("ln"+" "+"-s"+" "+"epel-5/"+" "+"epel-5Client")
		os.system("ln"+" "+"-s"+" "+"epel-5/"+" "+"epel-5Server")
		os.system("ln"+" "+"-s"+" "+"epel-5/"+" "+"epel-5Workstation")
		os.system("ln"+" "+"-s"+" "+"epel-5/"+" "+"epel-5.9")
		os.system("ln"+" "+"-s"+" "+"epel-5/"+" "+"epel-5.10")
		os.system("ln"+" "+"-s"+" "+"epel-5/"+" "+"epel-5.11")
	if k == "epel-6":
		os.system("ln"+" "+"-s"+" "+"epel-6/"+" "+"epel-6Client")
		os.system("ln"+" "+"-s"+" "+"epel-6/"+" "+"epel-6Server")
		os.system("ln"+" "+"-s"+" "+"epel-6/"+" "+"epel-6Workstation")
		os.system("ln"+" "+"-s"+" "+"epel-6/"+" "+"epel-6.1")
		os.system("ln"+" "+"-s"+" "+"epel-6/"+" "+"epel-6.2")
		os.system("ln"+" "+"-s"+" "+"epel-6/"+" "+"epel-6.3")
		os.system("ln"+" "+"-s"+" "+"epel-6/"+" "+"epel-6.4")
		os.system("ln"+" "+"-s"+" "+"epel-6/"+" "+"epel-6.5")
		os.system("ln"+" "+"-s"+" "+"epel-6/"+" "+"epel-6.6")
	if k == "epel-7":
		os.system("ln"+" "+"-s"+" "+"epel-7/"+" "+"epel-7Everything")
		os.system("ln"+" "+"-s"+" "+"epel-7/"+" "+"epel-7Server")
		os.system("ln"+" "+"-s"+" "+"epel-7/"+" "+"epel-7Workstation")
		os.system("ln"+" "+"-s"+" "+"epel-7/"+" "+"epel-7ComputeNode")
    print "Required links are created for epel dirs"
    return True

def post_spread(where):

    """
    :param: where:  The directory where Fedora and EPEL directories are created.
    """

    fedora_base = where+'/'+"Fedora"
    epel_base = where+"/"+"EPEL.repo"

    if not os.path.exists(fedora_base):
        os.makedirs(fedora_base)
    if not os.path.exists(epel_base):
        os.makedirs(epel_base)

    for dirs in os.listdir(where):
        cmd = "--backup --suffix \"-`date +\"%F-%T\"`\""
        if "fc" in dirs:
            print "Fedora:%s" %(dirs)
            os.system("mv"+ " "+where+"/fc*"+" "+fedora_base+" "+cmd)
        if "el" in dirs:
            print "EPEL.repo:%s" %(dirs)
            os.system("mv"+ " "+where+"/el*"+" "+epel_base+" "+cmd)

    print "Directory sorting done"
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

    destdir=os.path.abspath(destdir)
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
    fail = []
    os.chdir(sourcedir)
    task_ids = raw_input ("Enter path for taskid (ex:7034519):").split(",")
    task_id_list = [str(int(x)-1) for x in task_ids]
    print task_id_list
    count = int(raw_input("no of architectures:"))
    for task_id in task_id_list:
        cur_id =task_id
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
                print "Error occurred.. please check and re-run if required" + cur_id
                fail.append(cur_id)    
            else:
                print " \t Successfully downloaded.. Verify downloaded RPMS"
    if fail != []:
        print fail
        return False
    else:
        return True

def main():

    parser = OptionParser()
    parser.add_option("-p", "--pull",
                      action="store_true", dest="pull", default=False,
                      help="Pull packages from koji repo based on the taskid?")


    parser.add_option("-s", "--spread",
                      action="store_true", dest="spread", default=False,
                      help="Spread fedora and EPEL rpms from specified directory to approprite arch and distro")


    parser.add_option("-r", "--rearrange",
                      action="store_true", dest="rearrange", default=False,
                      help="Rearrange fedora and EPEL rpms from specified directory and sign rpms")

    parser.add_option("-l", "--link",
                      action="store_true", dest="link", default=False,
                      help="Create links for epel5,6,7 directories.")

    parser.add_option("-c","--repocreation",
                      action="store_true", dest="repocreation", default=False,
                      help="Creates repodata for Fedora and EPEL")

    parser.add_option("-a","--all",
                      action="store_true", dest="runall", default=False,
                      help="Runs all the commands")
    options, arguments = parser.parse_args()
    fedoradir=''
    epeldir=''
    anyopt = [ options.pull , options.spread, options.rearrange, options.link, options.repocreation, options.runall]
    check = [o for o in anyopt if o]
    if not check:
        print  "You missed one of the most required option.. re-read and execute.... exiting ."
        parser.print_help()

        sys.exit(1)

    if options.pull:
        print "action: pull"
        pull_dir = raw_input("Enter the directory path to pull packages :")
        pull_packages(pull_dir)

    if options.spread:
        print "action: spread"
        source_spread_dir = raw_input("Enter the source directory where the rpms are stored.:")

        dest_spread_dir = raw_input("Enter the destination directory where the rpms should be spread.:")

        spread_packages(source_spread_dir, dest_spread_dir)
    if options.rearrange:
	print "action:rearrange"
	source_rearrange_dir = raw_input("Enter the directory to rearrange:")
        source_rearrange_dir = os.path.abspath(source_rearrange_dir)
    	for dirs in os.listdir(source_rearrange_dir):
		if dirs == "EPEL.repo":
			epeldir = source_rearrange_dir+'/'+'EPEL.repo'
		elif dirs == "Fedora":
			fedoradir = source_rearrange_dir+'/'+'Fedora'
	if fedoradir == '' or epeldir == '':
                print "EPEL.repo or Fedora not found ... Exiting"
                sys.exit(1)
        rearrange_packages(fedoradir, epeldir)

    if options.link:
	print "action:link"
	source_link_dir = raw_input("Enter the directory (where EPEL.repo and Fedora are present): ")
        source_link_dir = os.path.abspath(source_link_dir)
    	for dirs in os.listdir(source_link_dir):
		if dirs == "EPEL.repo":
			epeldir = source_link_dir+'/'+'EPEL.repo'
		elif dirs == "Fedora":
			fedoradir = source_link_dir+'/'+'Fedora'
	if fedoradir == '' or epeldir == '':
                print "EPEL.repo or Fedora not found ... Exiting"
                sys.exit(1)
        os.mkdir(source_link_dir+"/CentOS")
        os.mkdir(source_link_dir+"/RHEL")
	os.system("ln"+" "+"-s"+" "+epeldir+"/* "+source_link_dir+"/RHEL")
	os.system("ln"+" "+"-s"+" "+epeldir+"/* "+source_link_dir+"/CentOS")
	link_creation(fedoradir, epeldir)

    if options.repocreation:
        print "action:repocreation"
        if not os.geteuid() == 0:
                sys.exit('Script must be run as root')
        source_repo_dir = raw_input("Enter the directory (where EPEL.repo and Fedora are present): ")
        source_repo_dir = os.path.abspath(source_repo_dir)
        for dirs in os.listdir(source_repo_dir):
                if dirs == "EPEL.repo":
                        epeldir = source_repo_dir+'/'+'EPEL.repo'
                elif dirs == "Fedora":
                        fedoradir = source_repo_dir+'/'+'Fedora'
	if fedoradir == '' or epeldir == '':
                print "EPEL.repo or Fedora not found ... Exiting"
                sys.exit(1)
        repo_creation(fedoradir,epeldir)
        os.mkdir(source_repo_dir+"/CentOS")
        os.mkdir(source_repo_dir+"/RHEL")
	os.system("ln"+" "+"-s"+" "+epeldir+"/* "+source_all_dir+"/RHEL")
	os.system("ln"+" "+"-s"+" "+epeldir+"/* "+source_all_dir+"/CentOS")

    if options.runall:
        print "action:all"
        ret = False
        condi = ''
        source_all_dir=raw_input("Enter the directory to pull the packages:")
        dest_all_dir=raw_input("Enter the directory where the EPEL.repo and Fedora should be stored:")
        curr_dir = os.getcwd()
        print "action:pull"
        ret = pull_packages(source_all_dir)
        if not ret:
                condi = raw_input("Enter 'y' to continue(anything to abort)")
                if condi != 'y':
                    sys.exit("Pull Packages Failed")
        print "\n action:pull *complete* \n\n action:spread"
        os.chdir(curr_dir)
        ret = spread_packages(source_all_dir,dest_all_dir)
        if not ret:
                sys.exit("Spread Packages Failed")
        print "\n action:spread *complete* \n\n action:rearrange"
        source_all_dir = os.path.abspath(dest_all_dir)
    	for dirs in os.listdir(source_all_dir):
		if dirs == "EPEL.repo":
			epeldir = source_all_dir+'/'+'EPEL.repo'
		elif dirs == "Fedora":
			fedoradir = source_all_dir+'/'+'Fedora'
	if fedoradir == '' or epeldir == '':
                print "EPEL.repo or Fedora not found ... Exiting"
                sys.exit(1)
        ret = rearrange_packages(fedoradir, epeldir)
        if not ret:
                sys.exit("Rearrange Packages Failed")
        print "\n action:rearrange *complete* \n\n action:linking"
        ret = link_creation(fedoradir, epeldir)
        if not ret:
                sys.exit("Link Creation Failed")
        print "\n action:linking *complete* \n\n action:repo-creation"
        ret = repo_creation(fedoradir, epeldir)
        if not ret:
                sys.exit("Repo creation Failed")
        print "\n action:repo creation *complete* \n\nALL ACTION COMPLETE"
        os.chdir(curr_dir)
        os.mkdir(source_all_dir+"/CentOS")
        os.mkdir(source_all_dir+"/RHEL")
	os.system("ln"+" "+"-s"+" "+epeldir+"/* "+source_all_dir+"/RHEL")
	os.system("ln"+" "+"-s"+" "+epeldir+"/* "+source_all_dir+"/CentOS")

if __name__ == '__main__':
    #print "Starting %s ......." % (__name__)
    main()
