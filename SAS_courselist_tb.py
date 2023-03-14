# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:21:04 2023

@author: u1130196
"""


import sqlite3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

#initiate firefox
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r'C:\Users\u1130196\geckodriver\geckodriver.exe', options=options)

#URL to scrape
driver.get("https://admin.sas.anu.edu.au/psp/csprod/EMPLOYEE/SA/c/ESTABLISH_COURSES.CLASS_ROSTER.GBL");

#Deal with login
WebDriverWait(driver, 5000).until(EC.element_to_be_clickable((By.NAME, "userid"))).send_keys("u1130196")
WebDriverWait(driver, 5000).until(EC.element_to_be_clickable((By.NAME, "pwd"))).send_keys("coffee friand work")
print('done it!!')
WebDriverWait(driver, 7000).until(EC.element_to_be_clickable((By.NAME,"Submit"))).click()
print('submitted!!!')

#wait for it...and switch to iframe
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath("//iframe[@id='ptifrmtgtframe']")))

#enter search details
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'CLASS_RSTR_SRCH_STRM'))).send_keys("3330")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'CLASS_RSTR_SRCH_SUBJECT'))).send_keys("EMSC")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'#ICSearch'))).click()
print('entered!!!')

#get table into dataframe
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@id='win0divSEARCHRESULT']//table"))) 
df=pd.read_html(driver.find_element_by_xpath("//td[@id='PTSRCHRESULTS0']").get_attribute('outerHTML'))[0]

#clean course names
df["coursename"]=df["Subject Area"].astype(str) +"_"+ df["Catalogue Number"].astype(str) +"_"+ df["Description"]+"_"+ df["Term"].astype(str)
df["coursename"]=df["coursename"].str.replace(r"\(.*\)","", regex = True).str.replace(' ','')
print(df)

#select coursename
allcourses=df.loc[:,"coursename"]
print (allcourses)

#connect database and create table
conn = sqlite3.connect('RSES_teaching.db')
cur=conn.cursor()
print("connected!")

for i in allcourses:
    try:
        sql_script=f'''CREATE TABLE {i}
            (
            id INTEGER NOT NULL PRIMARY KEY,
            uNumber char (25)
            );
            '''
        cur.execute(sql_script)
        conn.commit()

    except:
        print("nope")    
    
print(allcourses)
print("Tables are Ready")


 # Getting all tables from sqlite_master
sql_query = """SELECT name FROM sqlite_master
    WHERE type='table';"""
     
# executing our sql query
cur.execute(sql_query)
print("List of tables\n")
     
# printing all tables list
print(cur.fetchall())

conn.close()
