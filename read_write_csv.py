#!/usr/bin/env python3

import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r', newline='') as filereader:
    with open(output_file, 'w', newline='') as filewriter:
        header = filereader.readline()
        header_list = header.strip().split(',')
        print(header_list)
        filewriter.write(','.join(map(str,header_list)) + '\n')
        for row in filereader:
            row_list = row.strip().split(',')
            print(row_list)
            filewriter.write(','.join(map(str, row_list)) + '\n')

# map(func, itera) function map the function to each item in the iterable
# object.
# string.join function, joins each element in the iteration using  a
# seperator.

# in the command line:
# python script_name.py "path of input file" "path of output file"
# make python script executable: chmod +x script_name.py
