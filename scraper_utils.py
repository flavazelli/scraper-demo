from selenium import webdriver
from pymongo import MongoClient
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from item import Item

def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['local']
    collection = db['products']
    return collection

def setup_webdriver():
    options = uc.ChromeOptions()
    # options.add_argument("--headless=new")
    driver = uc.Chrome(options=options)
    driver = webdriver.Chrome(options=options)
    return driver

def launch_scraper(link, productClass, store, parseFunction):
    pageNumber = 1
    driver = setup_webdriver()
    collection = connect_to_mongodb()
    while True: 

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
                print(product)
        pageNumber += 1
        
    driver.quit()
