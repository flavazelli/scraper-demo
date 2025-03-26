from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from item import Item
import time
import random
import undetected_chromedriver as uc
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['local']
    collection = db['products']
    return collection

def setup_webdriver():

    if os.getenv('USE_STANDALONE_CHROME_DRIVER') == 'true':
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444',
        options=options
        )
    else:
        driver = uc.Chrome()
    return driver

def launch_scraper(link, productClass, store, parseFunction):

    pageNumber = 1
    driver = setup_webdriver()
    collection = connect_to_mongodb()
 
    while True: 
        time.sleep(random.randint(1,5))

        driver.get(f'{link}{pageNumber}')

        WebDriverWait(driver, 180).until(
            EC.visibility_of_element_located((By.CLASS_NAME, productClass))
        )

        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        products = soup.select(f".{productClass}")

        if not products:
            break

        for product in products:
            try:
                item = Item(store)
                parseFunction(product, item)
                collection.insert_one(item.to_mongo_dict())
            except Exception as e:
                print(e)
        pageNumber += 1
        
    driver.quit()
