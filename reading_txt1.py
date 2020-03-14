"""
Reading txt file

the sys module has variable argv which captures the list of command line
arguments, including your script name, passed to the python script. argv[0] is
the script name, argv[1] is the path to the file to be read by the python script
"""


"""1. traditional file reading which needs to close the file explicitly"""
import sys

'''
# read a single text file
input_file = sys.argv[1]

file_reader = open(input_file, 'r')

for row in file_reader:
    print('{}'.format(row.strip()))
file_reader.close()
'''

# in the terminal, cd to the folder, and use python scriptname.py
# filename.txt to execute.


"""2. modern way by using with open to open a file which closes the file 
automatically when the with statement is exited"""
'''
input_file = sys.argv[1]
with open(input_file, 'r', newline='') as file_reader:
    for row in file_reader:
        print('{}'.format(row.strip()))
'''

"""read multiple txt file under a folder, use the path of the directory as
argument
module os provides several pathname functions
module glob provides functions to find all pathname matching a specific pattern
"""

import os
import glob

input_directory_path = sys.argv[1]

for input_file in glob.glob(os.path.join(input_directory_path, '*.txt')):
    with open(input_file, 'r', newline='') as file_reader:
        for row in file_reader:
            print('{}'.format(row.strip()))


