As of now, "glusterpackager.py" is ONLY compatible with koji scratch builds.

```
[github]# python glusterpackager.py --help
Usage: glusterpackager.py [options]

Options:
  -h, --help          show this help message and exit
  -p, --pull          Pull packages from koji repo based on the taskid?
  -s, --spread        Spread fedora and EPEL rpms from specified directory to
                      approprite arch and distro
  -r, --rearrange     Rearrange fedora and EPEL rpms from specified directory
                      and sign rpms
  -l, --link          Create links for epel5,6,7 directories.
  -c, --repocreation  Creates repodata for Fedora and EPEL
  -a, --all           Runs all the commands 

```


