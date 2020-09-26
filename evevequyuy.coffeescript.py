import cv2
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.select import Select


# PATH = "C:/Program Files (x86)/chromedriver.exe"
# driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome()
driver.get("https://login.virgilio.it/key.phtml")

driver.find_element_by_id("loginid").send_keys("1nicoloperusino@virgilio.it")
driver.find_element_by_id("form_submit").click()
time.sleep(1)
driver.find_element_by_id("password").send_keys("Aeiou111")
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='qc-cmp2-ui']/div[2]/div/button[2]"))).click()
except selenium.common.exceptions.TimeoutException:
    c = 0

driver.find_element_by_id("form_submit").click()
time.sleep(5)
time.sleep(2)
WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "io-ox-topbar-dropdown-icon"))).click()

WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="topbar-settings-dropdown"]/li[4]/a'))).click()

# WebDriverWait(driver, 30).until(
#                 EC.presence_of_element_located((By.ID, 'folder-tree-386-node-431'))).click()
""" mi da errore"""

# WebDriverWait(driver, 30).until(
#                 EC.presence_of_element_located((By.XPATH, '//*[@id="window-1"]/div/div[4]/div/div[3]/div/div/div/button[2]/i'))).click()

sleep(5)
elemento_Posta = driver.find_elements_by_class_name("folder-arrow")[3]
elemento_Posta.click()