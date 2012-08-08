mv-elsewhere
============

Move a list of directories, possibly piped from "find" to semewhere else preserving directory tree and attributes.

why
===

Do you know this huge volume with terabytes of OLD data mixed with working data? This script will help moving those files to another location just piping in whatever "find" tells is old.

why not bash?
============

It is possible to do it with bash, but it gets complicated with some "user named files",... with nice characters...
...And I have to learn python! ;)

use
===
mv-elsewhere.py -d <destfile> [-m] [-o] [-v] [-D][-e string]

	-d: destination directory.
	-D: debug.
	-e: excluded sting. If file or path contain this string it will be excluded.
	-m: move files instead of copy.
	-o: override files in case of copy or move.
	-v: verbose.
	
Example:
find testdir -mtime +620  | /usr/local/bin/mv-elsewhere -d testdest -m -e excludestring


TODO
====
-add possibility to give multiple excludes
-add posibility to read files to process from a file instead of stdin
-add a staristics do nothing option,.. this option will actualy do nothing. Instead it will print what would do.

