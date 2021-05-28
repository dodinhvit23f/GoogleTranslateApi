import TranslateGoogleApi
import traceback
from multipledispatch import dispatch
import os
import pdb
import sys
import argparse
import time
import ChromeDriver
import pdb

def parse_arguments(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('--tgt_lang', type=str, help='Target Language.',default="km")
    parser.add_argument('--src_lang', type=str, help='Source Language.',default="vi")
    parser.add_argument('--translate_path', type=str, help='Translate path',default="./Translate/vi/")
    parser.add_argument('--save_path', type=str, help='Save path',default="./Translate" )
    return parser.parse_args(argv)

# python FileToFileTranslate.py --tgt_lang "lo" --src_lang "vi" --translate_path "./Translate/vi/DoiSong" --save_path "./Translate"
if __name__ == '__main__':
    parser = parse_arguments(sys.argv[1:])

    tgt_lang = parser.tgt_lang
    src_lang = parser.src_lang
    translate_path = parser.translate_path
    save_path =  parser.save_path +"/{}-{}/".format(src_lang, tgt_lang)

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    driver = ChromeDriver.getChromeDriver()
    url = "https://translate.google.com/?sl={}&tl={}&text={}&op=translate".format(src_lang, tgt_lang, "")
    driver.get(url)

    list_file = os.listdir(translate_path)
    loop = 0
    for file in list_file:
        if(loop == 1000):
            driver.close()
            driver = ChromeDriver.getChromeDriver()
            url = "https://translate.google.com/?sl={}&tl={}&text={}&op=translate".format(src_lang, tgt_lang, "")
            driver.get(url)
            loop = 0
            os.system("cls")
            
        if(file.find(".") != -1):
            list_text = list()
            if os.path.isfile(save_path+file):
                continue
            f = open(translate_path+"/{}".format(file), "r", encoding="utf-8")
            for line in f:

                line = line.replace("\n","")
                line = line.strip()

                if(line == "" or line == " "):
                    continue

                list_text.append(line)
            f.close()
           
            TranslateGoogleApi.translateFileToFileApi(driver=driver,  list_text=list_text, file_name=save_path+file)
            print(save_path+file)
            time.sleep(1)
            #pdb.set_trace()
            url = "https://translate.google.com/?sl={}&tl={}&text={}&op=translate".format(src_lang, tgt_lang, "")
            driver.get(url)
            loop = loop + 1
    driver.close()