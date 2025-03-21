from selenium import webdriver
from pymongo import MongoClient
import undetected_chromedriver as uc

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