# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:37:03 2023

@author: u1130196
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#initiate firefox
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r'C:\Users\u1130196\geckodriver\geckodriver.exe', options=options)

#URL to scrape
driver.get("https://u1130196:Hudson2022!@wattlecourses.anu.edu.au/course/view.php?id=39000");

#Deal with login
WebDriverWait(driver, 5000).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='header'][text()='Username and Password']"))).click()
print('success1')
WebDriverWait(driver, 5000).until(EC.element_to_be_clickable((By.NAME, "legacyAuthUsername"))).send_keys("u1130196")
WebDriverWait(driver, 5000).until(EC.element_to_be_clickable((By.NAME, "legacyAuthPassword"))).send_keys("Hudson2022!")
print('success2')
WebDriverWait(driver, 7000).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ui right floated button'][text()='Submit']"))).click()
print('success3')

#navigate to pages to scrap