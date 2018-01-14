#!/usr/bin/python3

"""
Import existing passwd file optionally ignoring system users
"""

from optparse import OptionParser, OptionError
import textwrap
import sys
import subprocess


def main():
    try:
        usage = textwrap.dedent("""
           %prog [OPTIONS]

           eg: %prog --min-uid 500 --filename /etc/passwd
        """)
        parser = OptionParser(usage=usage)
        parser.add_option("-m", "--min-uid", dest="minuid",
                          help="Minimum UID to include in import")
        parser.add_option("-f", "--filename", dest="importfile",
                          help="File in unix passwd format to import")
        parser.add_option("-s", "--service", dest="service",
                          help="Service to add imported file to in consul")

        (options, args) = parser.parse_args()
        parse_passwd(options, args)

    except OptionError as err:
        print(err)
        parser.print_help()
        sys.exit(2)


def parse_passwd(options, args):
    # Open file and loop over values
    f = open(options.importfile, "r")
    for line in f:
        # line format: brockp:x:158765:65540:Brock Edward Palen:/home/brockp:/bin/bash
        (username, x, uid, gid, comment, homedir, shell) = line.rstrip().split(':')

        # homedir needs to be just the prefix the Username
        #  The username is autoadded
        basedir = homedir.rstrip("/"+username)
        subprocess.check_call(["./useradd.py",
                               "--arcuser", username,
                               "--uid", uid,
                               "--gid", gid,
                               "--comment", comment,
                               "--base-dir", basedir,
                               "--shell", shell,
                               "--service", options.service
                               ])


if __name__ == "__main__":
    main()
