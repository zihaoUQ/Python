"""write to a file"""
import sys

'''
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
max_index = len(letters)
output_file = sys.argv[1]

file_writer = open(output_file, 'w')
# place delimiter (\t tab or , comma) between values, and a newline character
# after the last value
for i in range(max_index):
    if i < (max_index - 1):
        file_writer.write(letters[i] + '\t')
    else:
        file_writer.write(letters[i] + '\n')
file_writer.close()
print('output written to file. Done')
'''

"""append to the end of existing file using mode 'a' (append), and also
 using delimiter ',' for csv file
 use str() to convert non string values before writing to a file
 """

number = [0, 1, 2, 3, 4, 5]
max_index = len(number)
output_file = sys.argv[1]
# append mode 'a' to append to the end of existing file with contents
file_writer = open(output_file, 'a')
for i in range(max_index):
    if i < (max_index - 1):
        file_writer.write(str(number[i]) + ',')
    else:
        file_writer.write(str(number[i]) + '\n')
file_writer.close()
print('done')
