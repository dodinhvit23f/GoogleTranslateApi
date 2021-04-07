import collections
import re
import pdb

dir_ = {"" : ""}

f = open("vi-zh.dir.txt", "r", encoding="utf-8")
index = 0
for line in f:
    line = line.replace("\n","").strip()
    line = bytes(line,"utf-8").decode('utf-8', 'ignore')
    line = line.split("\t")
    #pdb.set_trace()
    index = index + 1
    if(len(line) == 1):
        print(index)
        continue
        
    if not line[1] in dir_:
        dir_[line[1].strip()] = line[0].strip()
f.close()

f = open("vi-zh.dir2.txt", "w", encoding="utf-8")
for key in  dir_:
    if(key != "" and key != " "):
        f.write("{}\t{}\n".format(dir_[key], key))
f.close()