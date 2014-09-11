#!/usr/bin/env python
# pulled from git 140911
# bad line endings have been removed with dos2unix   [20140831]
# that caused crazy reaction when using directly (using the shebang)
# 140831: shortened the exit if no dupes
#
# possible bug: if A contains B and dupes the songs from B(and also in dupes) will be destroyed
# need to test and correct by excluding dupes from base list
#
#
import os, sys, shutil
from os.path import join, getsize, exists
totsize = 0             #total Kbytes
L = []			# compare-to List
LB = []			# exclude List if B included in A so that: L inter LB = 0
AL =[]			# compare-to List for Absolute paths

# 1 ---------------- get dirs from cmd line or input. process ~ if any
if len (sys.argv) > 2:
	askdir1 = sys.argv[1]
	askdir2 = sys.argv[2]
else:
	print "\n [v6.7] If one dir is included in other, enter big one first -- start with '!' if under My Documents (windows) "
	askdir1 = raw_input ("Enter the  first dir's name (case sensitive) >> ")
	askdir2 = raw_input ("Enter the  other dir's name (case sensitive) >>")
	
if askdir1.startswith('!'):
	basedir = os.path.expanduser( '~')+'\\My Documents'  #base home dir
	askdir1 = basedir + '/' + askdir1[1:]

if askdir2.startswith('!'):
	basedir = os.path.expanduser( '~')+'\\My Documents'  #base home dir
	askdir2 = basedir + '/' + askdir2[1:]

# 2.1 --------- start scanning dir2 -- build exclude dir2 List!!
for root, dirs, files in os.walk(askdir2):
	LB += [os.path.abspath(join(root, name)) for name in files if name.endswith('.wma') or name.endswith('.mp3')]
	
# 2.2 --------- start scanning dir1 -- build compare-to List L - exclude dir2!!
for root, dirs, files in os.walk(askdir1):
    L += [name for name in files if (name.endswith('.wma') or name.endswith('.mp3')) and os.path.abspath(join(root, name)) not in LB]
    AL += [os.path.abspath(join(root, name)) for name in files if (name.endswith('.wma') or name.endswith('.mp3')) and os.path.abspath(join(root, name)) not in LB]
	
#  3 --------- start scanning dir2 -- print if match
print "\n\n --- DUPLICATED WMA AND MP3 FILES --- "
for root, dirs, files in os.walk(askdir2):
	for name in files:
		if name in L:
#			print join(root, name)[:20]+ ' ... ' + join(root, name)[-40:]
			print os.path.abspath(join(root, name))[-70:]
			totsize += getsize(join(root, name))/1024.0

print "\n*** Total Duplicated: %9.1f KB in %s" % (totsize, askdir2)


# --------- writing to txt ---
if totsize > 0:

        askfile = raw_input ("\n Write to a file?  y/[n] >>")
        if askfile.startswith('y'):
            print "\n\n writing to 'dupes.txt' now..."
            # Create a text/plain message
            f=open('./dupes.txt', 'w')
            for root, dirs, files in os.walk(askdir2):
	        for name in files:
		        if name in L:
			        f.write(os.path.abspath(join(root, name))+'\n')
        #			f.write(join(root, name)+'\n')
            f.close()
        #  --------- dupes copy and remove from askdir2 - MUST CHECK if DUPES DIR EXISTS
        print "\n\n Copy them to /dupes dir and remove them from "+askdir2,
        askfile = raw_input ("?  y/[n] >>")
        if askfile.startswith('y'):
            if exists('./dupes'):
                print "\n\n copying to ./dupes dir now..."
                for root, dirs, files in os.walk(askdir2):
                    for name in files:
                            if name in L:
                                    fname=join(root, name)
                                    if os.path.abspath(fname) in AL:
                                        print "--------------------scandal!! same file!"
                                    else:
                                        print "\n.. copying "+ fname
                                        shutil.copy(fname, './dupes/')
                                        os.unlink(fname)
                print "\n\n done."
            else:
                print "\n\n need to create that 'dupes' directory, dude..."


# end pause
#if len (sys.argv) < 2:   # necess. in win mode not in dos
#	raw_input ("\n\nPress a key  to Exit >>")
