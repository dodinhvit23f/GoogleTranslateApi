from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.opera.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import traceback
from multipledispatch import dispatch
import os
import pdb
import sys
import argparse
import time
import urllib
import re
import ChromeDriver
from selenium.webdriver import Chrome
from selenium import webdriver

def compareTitle(src_title, tgt_title):

    src_title = src_title.lower().strip()
    tgt_title = tgt_title.lower().strip()
    
    src_title = re.sub("[!.,@#$%^&*()?<>]","",src_title)
    tgt_title = re.sub("[!.,@#$%^&*()?<>]","",tgt_title)
    
   
    
    src_title = re.sub("\s+"," ",src_title)
    list_word = src_title.split(" ")
    
    
   
    count = 0
    for word in list_word:
        if(tgt_title.find(word) != -1):
            count = count + 1
            
    
    return(count/len(list_word))

def saveFile(translate_file_name, list_transed_text):

    f = open(translate_file_name,"a",encoding="utf-8")
    for text in list_transed_text:
        f.write("{}\t{}\n".format(text[0], text[1]))
    f.close()
    
def getTranslateContent(driver, list_tgt):

    try:
        time.sleep(1) 
        
        content_translate_text = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_class_name('J0lOec'))
        
        list_ = content_translate_text.text.split("\n")
            
        #print(list_)
        
        for x in list_:
            if(x == ""):
                list_.remove("")
            if(x == " "):
                list_.remove(" ")
        
        if (len(list_tgt) != len(list_)):
            return list()
            
        index = 0
        list_transed_text = list()
        
        print("Thanh Cong")
        
        for line in list_:
            if line != "" and line != " ":
                list_transed_text.append((line, list_tgt[index]))
                index = index + 1           
        
        return list_transed_text
    except:
        pass
@dispatch(str,str,list)
def translate(src_lang, tgt_lang, list_text):
    global translate_file_name
    
    list_tgt = list()
    
    count = 1
    search_text = ""
    sign = ";"
    #f = open("link.test.txt", "w", encoding="utf-8")
    loop = 1
    
    opera_profile = "C:\\Users\\\Admin\\AppData\\Roaming\\Opera Software\\Opera Stable"
    options = Options()
    options.binary_location = r'C:\Users\\Admin\AppData\Local\Programs\Opera\74.0.3911.107\opera.exe'
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    #options.add_argument('--user-data-dir=' + opera_profile)
    
    #driver = webdriver.PhantomJS(os.path.abspath(os.getcwd()+"\phantomjs"))
    #driver = webdriver.Opera(executable_path=os.path.abspath(os.getcwd()+"/operadriver.exe"), options = options)
    driver = ChromeDriver.getChromeDriver()
    
    url = "https://translate.google.com/?sl={}&tl={}&text={}&op=translate".format(src_lang, tgt_lang, "")
    driver.get(url)
    textarea = driver.find_element_by_tag_name("textarea")
    
    old_text = ""
    
    print(len(list_text))
    
    len_of_batch = 0
    lim_of_batch = 3800
    text_to_translate = ""
    
    list_transed_text = list()
    
    try:
        for text in list_text:
            
            if(loop % 100 == 0):
                driver.close()
                driver = ChromeDriver.getChromeDriver()
                url = "https://translate.google.com/?sl={}&tl={}&text={}&op=translate".format(src_lang, tgt_lang, "")
                driver.get(url)
                textarea = driver.find_element_by_tag_name("textarea")
                loop = 1
            
            textarea = driver.find_element_by_tag_name("textarea")
            
            if(len_of_batch > lim_of_batch):
                
                last_index = len(text_to_translate) - 1
                if(text_to_translate[last_index] == "\n"):
                    text_to_translate = text_to_translate[0:last_index - 1]
                textarea.send_keys(text_to_translate)
                
                list_transed_text = getTranslateContent(driver, list_tgt)
                
                textarea.clear()
                len_of_batch = 0
                
                text_to_translate = ""
                loop = loop + 1
                time.sleep(0.5)
                
                url = "https://translate.google.com/?sl={}&tl={}&text={}&op=translate".format(src_lang, tgt_lang, "")
                driver.get(url)
                
            else:
                text_len =  len(text)
                
                if(text_len + len_of_batch > 4000):
                
                    last_index = len(text_to_translate) - 1
                    if(text_to_translate[last_index] == "\n"):
                        text_to_translate = text_to_translate[0:last_index - 1]
                    
                    textarea.send_keys(text_to_translate)
                    
                    list_transed_text = getTranslateContent(driver, list_tgt)
                    
                    textarea.clear()
                    len_of_batch = 0                  
                    list_tgt = list()
                    loop = loop + 1
                    text_to_translate = ""
                    time.sleep(0.5)
                    
                    url = "https://translate.google.com/?sl={}&tl={}&text={}&op=translate".format(src_lang, tgt_lang, "")
                    driver.get(url)
                    
                    
                len_of_batch = len_of_batch + text_len
            
            text = bytes(text,"utf-8").decode('utf-8', 'ignore')
            text = text.replace("\r","")
            not_bmp = x = re.search(u'[\U00010000-\U0010ffff]', text)
            
            
            if not_bmp:
                continue
                
            text_to_translate = text_to_translate+text+" \n" 
            list_tgt.append(text)
            
            if list_transed_text:
                saveFile(translate_file_name,list_transed_text)
                list_transed_text = list()
               
    except Exception as e:
                print(e)
                traceback.print_exc()
                time.sleep(3)
                #pdb.set_trace()
                pass    
    #f.close()
    
    if(len_of_batch > 0):
        textarea.send_keys(text_to_translate)
        list_transed_text = getTranslateContent(driver, list_tgt)
        
    if  list_transed_text :
        if(len(list_transed_text) > 0):
            saveFile(translate_file_name,list_transed_text)        
    driver.close()



def translateFileToFileApi(driver, list_text, file_name):
    global translate_file_name

    
    loop = 1

    textarea = driver.find_element_by_tag_name("textarea")

    print(len(list_text))

    len_of_batch = 0
    lim_of_batch = 3800
    text_to_translate = ""
    
    list_tgt = list()
    list_transed_text = list()

    try:
        for text in list_text:

            if (len_of_batch > lim_of_batch):

                last_index = len(text_to_translate) - 1
                if (text_to_translate[last_index] == "\n"):
                    text_to_translate = text_to_translate[0:last_index - 1]
                textarea.send_keys(text_to_translate)

                list_transed_text = getTranslateContent(driver, list_tgt)

                textarea.clear()
                len_of_batch = 0
                list_tgt = list()
                text_to_translate = ""
                loop = loop + 1
                time.sleep(0.5)



            else:
                text_len = len(text)

                if (text_len + len_of_batch > 4000):

                    last_index = len(text_to_translate) - 1
                    if (text_to_translate[last_index] == "\n"):
                        text_to_translate = text_to_translate[0:last_index - 1]

                    textarea.send_keys(text_to_translate)

                    list_transed_text = getTranslateContent(driver, list_tgt)

                    textarea.clear()
                    len_of_batch = 0
                    list_tgt = list()
                    loop = loop + 1
                    text_to_translate = ""
                    time.sleep(0.5)

                len_of_batch = len_of_batch + text_len

            text = bytes(text, "utf-8").decode('utf-8', 'ignore')
            text = text.replace("\r", "")
            not_bmp = x = re.search(u'[\U00010000-\U0010ffff]', text)

            if not_bmp:
                continue

            text_to_translate = text_to_translate + text + " \n"
            list_tgt.append(text)

            if list_transed_text:
                saveFile(file_name, list_transed_text)
                list_transed_text = list()

    except Exception as e:
        print(e)
        traceback.print_exc()
        time.sleep(3)
        # pdb.set_trace()
        pass
        # f.close()

    if (len_of_batch > 0):
        textarea.send_keys(text_to_translate)
        list_transed_text = getTranslateContent(driver, list_tgt)
        
    if list_transed_text:
        if (len(list_transed_text) > 0):
            saveFile(file_name, list_transed_text)


@dispatch(str,str,list,list)    
def translate(src_lang, tgt_lang, list_text,list_compare):

    global translate_file_name
    
   
    if not list_compare:
        return
        
    print(len(list_text))
    
    index = 1
    for translated in list_compare:
        try:
            list_text.remove(translated)
            index = index + 1
        except:
            pdb.set_trace()
        print("loai cau: {}".format(translated))
        
    
    list_text = sorted(list_text, key=len)    
    translate(src_lang, tgt_lang, list_text)

    
@dispatch(dict, list, str)    
def getSentenceInFile(map_ , list_dir, current_dir):
    global tgt_lang
    
    list_dir = os.listdir(current_dir)
    
    for file in list_dir:
        if(file.find(".") == -1):
            
            getSentenceInFile(map_ , list_dir, current_dir+"/{}".format(file)) 
            
        elif(file.find("{}.txt".format(tgt_lang)) != -1) :
            
            f = open(current_dir+"/"+file, "r", encoding="utf-8")
            for sentence in f:
                #validate dữ liệu không tin 1 ai cả !!!
                sentence = sentence.replace("\n","").replace("\t\t","\t")
                if(sentence != ""):
                    #lọc từ bị trùng, do lười quá :))
                    map_[sentence] = 1
                    
            f.close()
@dispatch(dict)    
def getSentenceInFile(map_):

    current_dir = os.path.dirname(os.path.realpath(__file__))
    current_dir = current_dir
    list_dir = os.listdir(current_dir)
    
    for file in list_dir:
        if(file.find(".") == -1):
            getSentenceInFile(map_ , list_dir, current_dir+"/{}".format(file))

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
        
def parse_arguments(argv):

    parser = argparse.ArgumentParser()  
    parser.add_argument('--file_name', type=str, help='Source Language.',default="Translate-zh.txt")
    parser.add_argument('--save_file_name', type=str, help='Source Language.',default="vi-zh.txt")
    parser.add_argument('--tgt_lang', type=str, help='Target Language.',default="km")
    parser.add_argument('--src_lang', type=str, help='Source Language.',default="vi")
    parser.add_argument('--case', type=int, help='1 to crawl , 2 to translate',default=2)
    return parser.parse_args(argv)

# python TranslateGoogleApi.py --tgt_lang "zh" --case 2 --file_name "Translate-zh.txt" --save_file_name "vi-zh.txt"
# python TranslateGoogleApi.py --tgt_lang "km" --case 2 --file_name "Translate-km.txt" --save_file_name "vi-km.txt"
# python TranslateGoogleApi.py --tgt_lang "lo" --case 2 --file_name "Translate-lo.txt" --save_file_name "vi-lo.txt"
# python TranslateGoogleApi.py  --src_lang "vi" --tgt_lang "km" --case 2 --file_name "test.txt" --save_file_name "km-vi.txt"
# python TranslateGoogleApi.py  --src_lang "vi" --tgt_lang "zh-CN" --case 2 --file_name "test.txt" --save_file_name "zh-vi.txt"
# python TranslateGoogleApi.py  --src_lang "vi" --tgt_lang "lo" --case 2 --file_name "test.txt" --save_file_name "lo-vi.txt"
if __name__ == '__main__':
    
    parser = parse_arguments(sys.argv[1:])
    
    tgt_lang = parser.tgt_lang
    src_lang = parser.src_lang
    
    if(parser.case == 1):
        file_name = parser.file_name
        list_ = list()
        if not os.path.isfile(file_name):
            map_ = {"":""}
            getSentenceInFile(map_)
            list_ =  list(map_.keys())
            f = open(file_name, "w", encoding ="utf-8")
            
            for text in list_:
                if(text != ""):
                    f.write("{}\n".format(text))
            f.close()
            
    if(parser.case == 2):
    
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
    
        file_name = parser.file_name
        translate_file_name = parser.save_file_name
        
        list_tgt = list()
        if not os.path.isfile(file_name):
            map_ = {"":""}
            getSentenceInFile(map_)
            list_tgt =  list(map_.keys())
            f = open(file_name, "w", encoding ="utf-8")
            
            for text in list_tgt:
                if(text != ""):
                    f.write("{}\n".format(text))
            f.close()
          
        else:
            print("doc file")
            f = open(file_name, "r", encoding ="utf-8")
            for sentence in f:
                sentence = sentence.replace("\n", "")
                sentence = bytes(sentence,"utf-8").decode('utf-8', 'ignore')
                #sentence = re.sub(u'[\u0000-\uFFFF]', "", sentence)
                if(sentence != "" or sentence != " "):
                    sentence = bytes(sentence,"utf-8").decode('utf-8', 'ignore')
                    list_tgt.append(sentence)
            f.close()
            
        
        if not os.path.isfile(translate_file_name):
            translate(src_lang, tgt_lang, list_tgt)
        else:
            list_need_trans_text = list()
            
            while( os.access(translate_file_name, os.R_OK) == False):
                time.sleep(1)
                
            f = open(translate_file_name,"r",encoding="utf-8")
            
            for text in f:
                text = text.replace("\n","").strip()
                text = text.split("\t")
                
                if(len(text) == 1):
                    print(len(list_need_trans_text))
                    continue
                    
                if(text[1] != "" or text[1] != " "):
                    list_need_trans_text.append(text[1])
            f.close()
            
            
            
            translate(src_lang, tgt_lang, list_tgt, list_need_trans_text)

            if(tgt_lang == "vi"):
                dict_lang = dict()
                
                f = open(translate_file_name,"r",encoding="UTF-8")
                
                for line in f:
                    line = line.replace("\n", "")
                    line = line.split("\t")
                    dict_lang[line[0]] = line[1]
                f.close()
                
                Validate(dict_lang, dic_list)
                
                f = open(translate_file_name,"w",encoding="UTF-8")
                
                for key in dict_lang:
                    f.write("{}\t{}\n".format(key, dict_lang[key]))
                f.close()
        