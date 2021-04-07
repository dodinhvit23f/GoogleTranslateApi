from selenium.webdriver.support.ui import WebDriverWait
import traceback
from multipledispatch import dispatch
import os
import pdb
import sys
import argparse
from selenium.webdriver.opera.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib
import re
import random

def WriteReport(driver, full_name):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSe92Nytu0NVxYIDKSz-CzuqdzKVOyE0vImAsR0uVEKFxg20tA/viewform?fbclid=IwAR30xkzMepAtajoQ8QJgs14hBGBHnJw6zYDlizhMQT_KGUdsPwuczg3AmdE")
    input_tag = driver.find_element_by_xpath("//input[@class='quantumWizTextinputPaperinputInput exportInput']")
    div_tags = driver.find_elements_by_xpath("//div[@class='freebirdFormviewerViewNumberedItemContainer']")
    input_tag.send_keys(full_name)
    
    button_send = driver.find_element_by_xpath("//div[@jscontroller='VXdfxd']")
    
    for div_tag in div_tags:
        
        
        
        radio_buttons = div_tag.find_elements_by_xpath(".//div[@jscontroller='EcW08c']")
        random_num = random.randint(1, 10000)
        
        if radio_buttons:
            
            max_radio = len(radio_buttons)
            postion = random_num % max_radio
            
            if(max_radio > 3):
                while (postion < 2):
                    random_num = random.randint(1, 10000)
                    postion = random_num % max_radio
            
            radio_buttons[ postion ].click()
           
    button_send.click()
    
if __name__ == '__main__':
    options =  webdriver.ChromeOptions()
     
    driver = webdriver.Chrome(executable_path=os.path.abspath(os.getcwd()+"/chromedriver.exe"), options = options)
    
    list_full_name = list()
    
    f = open("file-name.txt", "r", encoding = "utf-8")
    for line in f:
        line = line.replace("\n","");
        list_full_name.append(line)
    f.close()
    
    for full_name in list_full_name:
        try:
            WriteReport(driver, full_name)
        except:
            pass
    
    driver.close()