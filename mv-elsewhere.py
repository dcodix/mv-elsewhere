#! /usr/bin/env python

# Copyright (C) 2012 dcodix 

# This file may be distributed and/or modified under the terms of
# the GNU General Public License version 2 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.GPL" in the source distribution for more information.

""" This script will take filenames from the stdin and copy/move them to a
directory destination preserving the directory tree and atributes.

Most of the functionality is taken from shutil module.
"""

import os
import sys
import stat
import errno
import getopt
import argparse
from shutil import *
import time


def copydirtree(src, dst, symlinks=False, ignore=None, copy_function=copy2,
             ignore_dangling_symlinks=False):
    """This function is a modification of shutil copytree
    which only copy the directories of a tree but not
    the files or links.
    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        if os.path.isdir(srcname):
            copydirtree(srcname, dstname, symlinks, ignore, copy_function)
        else:
            continue
    try:
        copystat(src, dst)
    except OSError as why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)

def printmessage(logstring):
    print('['+str(time.time())+'] '+logstring)
def verbosemessage(logstring):
    if verbose:
        printmessage(logstring)
def debugmessage(logstring):
    if debuging:
        printmessage(logstring)

def main():
    scriptname = 'mv-elsewhere.py'
    dst = ''
    filemove = False
    override = False
    readstdin = True
    global verbose
    global debuging
    verbose = False
    debuging = False
    exclude = ''
    excludelist = ''

    #GET ARGS
    parser = argparse.ArgumentParser(description='Move files')
    parser.add_argument('-d', '--destdir', nargs=1, help='destination directory')
    parser.add_argument('-D', '--debuging', help='debug', action="store_true")
    parser.add_argument('-m', '--move', help='move instead of copy', action="store_true")
    parser.add_argument('-o', '--override', help='override in destination', action="store_true")
    parser.add_argument('-v', '--verbose', help='verbose', action="store_true")
    parser.add_argument('-e', '--exclude', nargs='+', help='esclude list')
    args = parser.parse_args()

    if args.destdir:
	    dst = args.destdir[0]
    if args.debuging:
	    verbose = True
	    debuging = True
    if args.move:
        filemove = True
    if args.override:
        override = True
    if args.verbose:
	    verbose = True
    if args.exclude:
        excludelist = args.exclude


    # PROCESS
    nfiles = 0
    while True:
        excludefile = False
        if readstdin: #This condition is meant to add the future posibility to read files directly from a file instead of stdin.
            file1 = sys.stdin.readline()
        if not file1:
            break
        file1 = file1.rstrip()
        debugmessage('file '+file1)
        fpath = os.path.dirname(file1)
        if len(fpath) == 0:
            fpath = file1
        if debuging:
            print('fpath '+fpath)
        if len(excludelist) != 0:
            for exclude in excludelist:
                if exclude in file1:
                    excludefile = True
                    debugmessage('file '+file1+' will be excluded')
        dfile = dst + '/' + file1
        dpath = dst + '/' + fpath
        if not os.path.isdir(dpath):
            verbosemessage('COPYNG TREE: from '+fpath+' to '+dpath)
            copydirtree(fpath, dpath)
        if not os.path.isdir(file1) and not excludefile:
            if not os.path.exists(dfile) or override:
                if filemove:
                    verbosemessage('MOVING: '+file1+' to '+dfile)
                    move(file1, dfile)
                    nfiles = nfiles + 1
                else:
                    verbosemessage('COPYING: '+file1+' to '+dfile)
                    copy2(file1, dfile)
                    nfiles = nfiles + 1
            else:
                verbosemessage('NOT OVERRIDING: '+dfile)
                pass
        else:
            if excludefile:
                verbosemessage('EXCLUDED: '+file1)
            pass
    if nfiles == 0:
        printmessage('No files have been moved or copied.')
    else:
        if filemove:
            printmessage(str(nfiles)+' files have been moved.')
        else:
            printmessage(str(nfiles)+' files have been copied.')

if __name__ == "__main__":
    main()
