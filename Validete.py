import pdb
import re
file = open("Translate-vi.txt", "r", encoding="utf-8")

dirc = dict()

oldtext = ""

for line in file:
    
    line = line.replace("\n","")
    """
    line = re.sub("[-]{2,}"," ", line)
    
    line = re.sub("[.]{4,}"," ", line)
    line = re.sub("[…]{4,}","", line)
    
    line = line.split("\t")
    """
    if(line != "\n" and line != " \n"):
        if not line in dirc:
            dirc[line] =  1
    

file.close()
list_ = list(dirc.keys())
list_ =  sorted(list_, key=len) 
file = open("Translate-vi1.txt", "w", encoding="utf-8")
for item in list_:
    if(item != ""):
        #file.write("{}\t{}\n".format(dirc[item], item))
        file.write("{}\n".format(item) )
file.close()    
