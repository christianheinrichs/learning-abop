#!/usr/bin/env python2

import os
import time
import zipfile

# Taken from https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory-in-python#1855118
# This function is the approximate equivalent of UNIX's zip -r parameter
# It recursively archives all files and folders specified
def zipdir(path, zip_object):
    """
        zipdir() takes two arguments: path and zip_object
        path is the current directory zipdir() is currently working on
        e.g. '/Users/swa/notes'
        zip_object is the ZipFile class object which gets passed to zipdir()
    """
    # Iterate with root, dirs, files trough the os.walk() tuple values
    # dirpath, dirnames and filenames. Tuple: (dirpath, dirnames, filenames)
    # dirpath is a string showing the current directory
    # dirnames is a list containing the directories of the current directory
    # filenames is a list of files in the current directory
    for root, dirs, files in os.walk(path):
        # Iterate with single_file trough the files list
        for single_file in files:
            # Write every file contained in the current directory to the
            # archive in this format:
            # 'root/single_file' e.g. '/Users/swa/notes/notes.py'
            zip_object.write(os.path.join(root, single_file), compress_type=zipfile.ZIP_DEFLATED)
    # While the UNIX command zip returns 0 automatically on success,
    # it has to be defined manually here
    return 0

# 1. The files and directories to be backed up are specified in a list.
# Example on Windows:
# source = ['"C:\\My Documents"', 'C:\\Code']
# Example on Mac OS X and Linux:
#source = ['/Users/swa/notes']
source = ['chapter-11', 'chapter-12']
# Notice we had to use double quotes inside the string
# for names with spaces in it.

# 2. The backup must be stored in a main backup directory
# Example on Windows:
# target_dir = 'E:\\Backup'
# Example on Mac OS X and Linux:
#target_dir = '/Users/swa/backup'
target_dir = 'backup'
# Remember to change this to which folder you will be using

# Create target directory if it is not present
if not os.path.exists(target_dir):
    os.mkdir(target_dir) # Make directory

# 3. The files are backed up into a zip file.
# 4. The current day is the name of the subdirectory in the main directory.
today = target_dir + os.sep + time.strftime('%Y%m%d')
# The current time is the name of the zip archive.
now = time.strftime('%H%M%S')

# Take a comment from the user to create the name of the zip file
comment = raw_input('Enter a comment --> ')
# Check if a comment was entered
if len(comment) == 0:
    target = today + os.sep + now + '.zip'
else:
    target = today + os.sep + now + '_' + \
             comment.replace(' ', '_') + '.zip'

# Create the subdirectory if it isn't already there
if not os.path.exists(today):
    os.mkdir(today)
    print 'Successfully created directory', today

# 5. We use the zip command to put the files in a zip archive
zf_object = zipfile.ZipFile(target, 'w')

# Run the backup
print "Zip command is:"
# This for loop is neccessary to get the individual values out of the
# source list and format them as function argument
for x in source:
    zip_command = "zipdir({0}, {1})".format(x, zf_object)
    print zip_command
print "Running:"

# We have to iterate through the list now instead of joining the strings,
# because there are problems with the usage of os.walk() on
# whole lists instead of the single values in source
for x in source:
    zip_command = zipdir(x, zf_object)
zf_object.close()

if zip_command == 0:
    print 'Successful backup to', target
else:
    print 'Backup FAILED'
