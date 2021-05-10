from selenium.webdriver.support.ui import WebDriverWait
import traceback
from multipledispatch import dispatch
import os
import pdb
import sys
import argparse
from selenium.webdriver.opera.options import Options
from selenium import webdriver
import time
import urllib
import re
import json


def translate(driver, src_lang, tgt_lang, text, name, dic_list):
    global translate_file_name
    global loop
    
    list_transed_text = list()
    list_tgt = text.split("\n")
    
    textarea = driver.find_element_by_tag_name("textarea")
    
    try:

        if(loop % 1000 == 0):
            driver.close()
            driver = webdriver.Opera(executable_path=os.path.abspath(os.getcwd()+"/operadriver.exe"))
            url = "https://translate.google.com/?sl={}&tl={}&text={}&op=translate".format(src_lang, tgt_lang, "")
            driver.get(url)
            textarea = driver.find_element_by_tag_name("textarea")
        
        print(loop)
        
        #list_tgt.append(text)
        
        text = bytes(text,"utf-8").decode('utf-8', 'ignore')              
        #           
        #search_text = urllib.parse.quote_plus(search_text)
        
        #f.write(url+"\n")
        
        textarea.send_keys(text)
        
        time.sleep(4)
        len_ = len(text)   
            
        content_translate_text = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_class_name('J0lOec'))
       
        list_ = content_translate_text.text.split("\n")
        list_.remove(" ")
        
        if(len(list_tgt) == len(list_)):
            index = 0
            f = open ("./Translated/{}.txt".format(name), "w", encoding="utf-8")
            for text in list_tgt:
                
                src_array = re.sub("[\^\#\^\$\!\~\`\-\(\)\\\.\,\:\?\/\!\@\{\}\"\;\'\“\[\]\"\+\_\*\…\’\”\«\‐\=\‘\–]", " ", list_[index])
                src_array = re.sub("\s+", " ", src_array)
                src_array = src_array.lower().split(" ")
                
                if not src_array:
                    index = index + 1
                    continue
                    
                keepSentence = True
                # mảng các từ trong 1 câu sau khi dịch
                for ele in src_array:
                    if(ele =="" or ele == " "):
                        continue
                    # các từ không đúng với định dạng
                    if not re.search("[A-z0-9]+",ele):
                        isVi = False
                        # kiểm tra trong từ điển xem có từ này không
                        for src_text in dic_list:
                            if( src_text == ele):
                                isVi = True
                                break
                                
                        if not isVi:
                            keepSentence = False
                            print(ele)
                            index = index + 1
                            break
                
                if not keepSentence:
                    continue
                
                if text != "" and text != " " and list_[index] != "" and list_[index] != " ":
                    f.write("{}\t{}\n".format(text, list_[index]))
                index = index + 1
            f.close()
        textarea.send_keys("\"")        
        textarea.clear()
        
        loop = loop + 1   
    except Exception as e:
                print(e)
                traceback.print_exc()
                time.sleep(3)
                pass 

def parse_arguments(argv):

    parser = argparse.ArgumentParser()  
    parser.add_argument('--tgt_lang', type=str, help='Target Language.',default="km")
    parser.add_argument('--src_lang', type=str, help='Source Language.',default="vi")
    return parser.parse_args(argv)
    
def Validate(dict_lang, dic_list):
    list_ = list()
    for key in dict_lang:
    
        if(key == "" or key == " "):
            continue
            
        # các từ không đúng với định dạng
        if not re.search("[A-z0-9]+", key):
            isVi = False
            # kiểm tra trong từ điển xem có từ này không
            for src_text in dic_list:
                if( src_text == key):
                    isVi = True
                    break
                    
            if not isVi:
                keepSentence = False
                
                list_.append(key)
                
                
                break
                
    for key in  list_:           
        dict_lang.pop(key, None) 
    
#python Translate.py   --tgt_lang "km" --src_lang "vi"
#python Translate.py   --tgt_lang "lo" --src_lang "vi"
if __name__ == '__main__':
    
    dirc_file_name = "vi.dir.txt"
    dic_list = dict()
    if os.path.isfile(dirc_file_name):
        f = open (dirc_file_name, "r", encoding ="utf-8")
        for line in f:
            line = line.replace("\n","")
            if not line in dic_list:
                dic_list[line] = 1
        f.close()

        if not dic_list:
            print("Missing vietnames dictionary file")
            quit()
            
    dict_ = dict()
    f = open("vi-lo.txt", "r", encoding="utf-8")
    
    for line in f:
    
        line = line.replace("\n", "")
        line = line.split("\t")
        
        dict_[line[0]] = line[1]
        
    f.close()
    
    Validate(dict_, dic_list)
    
   
    
    f = open("vi-lo1.txt", "w", encoding="utf-8")
    for key in dict_:

        if dict_[key]:
            f.write("{}\t{}\n".format(key, dict_[key]))
    
    f.close()
