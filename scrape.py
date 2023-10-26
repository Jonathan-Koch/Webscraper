import time
import signal

import sys
import os

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import pandas as pd


def signal_handler(sig, frame):
    print("You pressed CTRl C")
    ext = input("Are you sure you want to exit? ")
    if ext.lower() == "yes":
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def safe_to_excel(df, filename):
    while True:
        try:
            df.to_excel(filename, index=False)
            break
        except PermissionError:
            print(f"Permission denied when writing to {filename}. Retrying in 5 seconds...")
            time.sleep(5)

def scrape_and_save():
    login_url = "" #Enter url of login page to bypass login page
    
    chrome_driver_path = r'' #Enter your chrome driver path
    s = Service(chrome_driver_path)

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(login_url)

    # Replace 'username_css_selector' and 'password_css_selector' with the actual CSS selectors of the fields
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "")))
    username.send_keys("") #Enter your username

    # Fill in the password
    password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '')))    
    password.send_keys("") #Enter your password

    # Simulate pressing Enter
    password.send_keys(Keys.RETURN)# Fill in the password
    password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '')))    
    password.send_keys("")

    # Simulate pressing Enter
    password.send_keys(Keys.RETURN)

    time.sleep(5)

    urlpage = '' #Enter your url
    driver.get(urlpage)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    
    # Wait for the table to be present
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "")))

    source_data = driver.page_source
    bs_data = BeautifulSoup(source_data, 'html.parser')
    
    # Find the table
    # Find the table by its ID
    table = bs_data.find('table', {''})

    
    data = []
    
    # Iterate over each table row
    for row in table.findAll(''):
        # Find all the columns in the row
        cols = row.findAll('')
        
        # Extract text from each column
        cols_text = [col.text.strip() for col in cols]
        
        # Append the columns text to the data list
        data.append(cols_text)

    new_df = pd.DataFrame(data)

    # Write the new data to a temporary Excel file
    temp_filename = 'temp.xlsx'
    safe_to_excel(new_df, temp_filename)

while True:
    scrape_and_save()
    time.sleep(20)

