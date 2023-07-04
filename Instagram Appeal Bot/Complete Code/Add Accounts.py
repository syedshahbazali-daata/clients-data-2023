import os
import time, csv
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc  # pip install undetected-chromedriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pickle




options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()
driver.get('https://www.instagram.com/')
input('PLEASE LOGIN TO INSTAGRAM AND PRESS ENTER TO CONTINUE: ')
username = input('Enter username: ')

# save cookies to Accounts folder
pickle.dump(driver.get_cookies(), open(f'Accounts/{username}.pkl', 'wb'))
driver.quit()


