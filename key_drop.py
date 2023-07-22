#!/usr/bin/env python
# coding: utf-8

'''
    Author : Rubens (The University of Home)
   
   This bot can:-
   x. Search for tweets containing golden codes
   1. Send a message with a key-drop code to a channel (maybe telegram) 
   2. access a site called key-drop, wich allows you to input a golden code
   3. Trys to input a key-drop code (if no captcha was received)
'''
import sys
import csv
import requests
from time import sleep
import platform

import register
import telbot as tbot

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class Sites_list():
    def __init__(self):
        # Create an instance of the opend csvfile
        self.csv_file = open('db.csv', 'r')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_reader = csv.reader(self.csv_file)
        self.sites = []

        print(f"\_ Variables initiated: {[self.csv_file.readlines]}, {self.csv_writer}, {self.csv_reader}")

    # gets the list of sites from the file called db.csv
    def handle_db(self, site="twitter"):
        '''
        gets the list of sites from the file called db.csv
        :param site:
        :return:
        '''
        arquivo = self.csv_reader
        print(f"\_ Cade?? {arquivo}")
        for row in arquivo:
            print(f"|_ row in file db.csv {row}")
            
            if row[0] == "twitter":
                # print(site, row[1])
                print(f'|_ site sendo acessado: {row}')
                return row[1]

    def getSites(self):
        '''
        get the list of sites from the file called db.csv
        '''

        arquivo = self.csv_reader
        # Reads and returns a list of sites
        site_list = []
        for i, row in enumerate(arquivo):
            if i > 0:
                site_list.append(row[1])
        print(f"|_ Rows on csv_reader object of db.csv: {site_list}")

        self.sites = site_list
        return site_list
        
    


def get_keydrop_code():
    '''
    Actions: 
        1. Access twitter to get the code and send it to telegram_handler
        2. Access discord to get the code and send it to telegram_handler
        3. Record both codes on a csv file for future processing 
    '''
    sleepDelay = 5
    retrys=10
    window_size = "1920,1080"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

    options = Options()
    options.add_argument("start-maximized")
    options.headless = True
    # options.add_argument("--headless")
    if platform.system() != 'Windows':
        options.add_argument("--no-sandbox")

    options.add_argument(f'user-agent={user_agent}')
    options.add_argument(f"--window-size={window_size}")
    options.add_argument("--ingore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # def wait_and_find_elements_by_xpath(xpath, timeout=retrys) -> None:
    #     sleep(sleepDelay)
    #     for i in range(timeout):
    #         try:
    #             ele = driver.find_elements_by_xpath(xpath)
    #         except:
    #             sleep(sleepDelay)
    #         else:
    #             print(ele)

    def get_from_twitter() -> bool:
        try:
            print("\_ reading site list")
            sl = Sites_list()
            # print( f"|_ sites in file: {sl.getSites()}" )
            x_arg = '//span'
            url = sl.handle_db()
            print(f"\_ atribuindo site {url} ao driver")
            driver.implicitly_wait(15)
            driver.get(url)
            wait = WebDriverWait(driver, 1200)
            # wait the site to fully load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
            last_twitter_post = wait.until(
                EC.presence_of_element_located((By.XPATH, x_arg)))
                
            
            articles = last_twitter_post.find_elements(By.XPATH, '//article[@role="article"]')
            
            for article in articles: 
                text_content_chunk = article.text
                # print(text_content_chunk)
                found_code_article = any( a in text_content_chunk for a in ["Golden Code"])
                if found_code_article:
                    
                    print("\_ found code article")
                    article.click()
                    sleep(8)
                    break
                    
            comments = driver.find_elements(By.XPATH, "//span")
            
            for comment in comments:
                comment_txt = comment.text
                # print(f"\_ Tested comment text: {comment_txt}")
                if comment_txt.isalnum() and len(comment_txt) == 17:
                    code = comment_txt.upper()
                    print(f"\_ Code found! {code}") 
                    print(f"\_ Writing it to the csv file and sending it to the telegram bot chat.")
                    r = register.CodeCollector()
                    r.add_code(code)
                    r.get_codes()
                    tbot.send_it(code)
                    sleep(5)
                    return False

            return True
                
        except Exception as e:
            print(f"\_ Some bullshit just occured: {e}")
            return True

    
    return get_from_twitter()

