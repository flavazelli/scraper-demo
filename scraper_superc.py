# filepath: /scraper-demo/scraper_superc.py
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from random import randint as rand
from pymongo import MongoClient
from item import Item
from scraper_utils import connect_to_mongodb, setup_webdriver

# Connect to MongoDB
collection = connect_to_mongodb()
driver = setup_webdriver()

pageNumber = 1

while True: 
   time.sleep(rand(1, 5))
   driver.get(f'https://www.superc.ca/en/search-page-{pageNumber}')
   WebDriverWait(driver, 180).until(
      EC.visibility_of_element_located((By.CLASS_NAME, "tile-product"))
   )

   pageSource = driver.page_source
   soup = BeautifulSoup(pageSource, 'html.parser')
   products = soup.select(".tile-product")
   rows = []

   if not products:
      break

   for product in products:
      item = Item('superc')
      if 'data-product-brand' in product.attrs:
         item.brand = product.attrs['data-product-brand']
      if 'data-product-name' in product.attrs:
         item.name = product.attrs['data-product-name']
      if product.find('span', class_='head__unit-details'):
         item.size = product.find('span', class_='head__unit-details').text
      if product.find('span', class_='price-update') and not product.find('span', class_='pi-price-promo'):
         priceReg = re.search(r'\$([^$\/]*)', product.find('span', class_='price-update').text)
         if priceReg:
            item.regular_price = priceReg.group(1)
      elif product.find('span', class_='price-update') and product.find('span', class_='pi-price-promo'):
         priceReg = re.search(r'(?<=\$)(\d+(\.\d{1,2})?)', product.find('div', class_='pricing__before-price').text)
         if priceReg:
            item.regular_price = priceReg.group(1)
         salePriceReg = re.search(r'\$([^$\/]*)', product.find('span', class_='pi-price-promo').text)
         if salePriceReg:
            item.sale_price = salePriceReg.group(1)

      
      priceMatchPerKg = re.search(r'\$([^$\/]*)\/kg', product.text)
      if priceMatchPerKg:
         item.price_per_kg = priceMatchPerKg.group(1) 
      
      priceMatchPerUnit = re.search(r'\$([^$\/]*)\/un', product.text)
      if priceMatchPerUnit:
         item.price_per_unit = priceMatchPerUnit.group(1)
      
      priceMatchPer100g = re.search(r'\$([^$\/]*)\/100g', product.text)
      if priceMatchPer100g:
         item.price_per_100g = priceMatchPer100g.group(1)

      priceMatchPer100ml = re.search(r'\$([^$\/]*)\/100ml', product.text)
      if priceMatchPer100ml:
         item.price_per_100ml = priceMatchPer100ml.group(1)

      # Write to MongoDB
      collection.insert_one(item.to_mongo_dict())

   pageNumber += 1

driver.quit()