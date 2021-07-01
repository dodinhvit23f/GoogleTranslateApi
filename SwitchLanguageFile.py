import argparse
import sys


parser = argparse.ArgumentParser()  
parser.add_argument('--file_name', type=str, help='Source Language.',default="en-vi.txt")

argv = parser.parse_args(sys.argv[1:])

list_line = list()

file = open(argv.file_name, "r",encoding = "utf-8")
for line in file:
    line = line.replace("\n","")
    line = line.split("\t")
    list_line.append( (line[1],line[0] ) )
file.close()

file = open(argv.file_name, "w",encoding = "utf-8")
for line in list_line:
    file.write("{}\t{}\n".format(line[0], line[1]))
file.close()