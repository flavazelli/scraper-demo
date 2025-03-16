# filepath: /scraper-demo/scraper_superc.py
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import csv
from random import randint as rand
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['local']
collection = db['products']
options = webdriver.ChromeOptions()

options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

with open('superc_scrape.csv', mode='w', newline='', encoding='utf-8') as csvFile:
   csvWriter = csv.writer(csvFile)
   csvWriter.writerow(['title', 'size', 'regular price', 'sale price', 'price/unit', 'price/kg', 'price/100g', 'price/100ml'])

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
      title = ""
      size = ""
      brand = ""
      price = ""
      salePrice = float()
      pricePerKg = float()
      pricePerUnit = float()
      pricePer100g = float()
      pricePer100ml = float()

      if 'data-product-brand' in product.attrs:
         brand = product.attrs['data-product-brand']

      if 'data-product-name' in product.attrs:
         title = product.attrs['data-product-name']
      
      if product.find('span', class_='head__unit-details'):
         size = product.find('span', class_='head__unit-details').text

      if product.find('span', class_='price-update'):
         priceReg = re.search(r'\$([^$\/]*)', product.find('span', class_='price-update').text)
         if priceReg:
            price = priceReg.group(1)
      
      priceMatchPerKg = re.search(r'\$([^$\/]*)\/kg', product.text)
      if priceMatchPerKg:
         pricePerKg = priceMatchPerKg.group(1)
      
      priceMatchPerUnit = re.search(r'\$([^$\/]*)\/un', product.text)
      if priceMatchPerUnit:
         pricePerUnit = priceMatchPerUnit.group(1)
      
      priceMatchPer100g = re.search(r'\$([^$\/]*)\/100g', product.text)
      if priceMatchPer100g:
         pricePer100g = priceMatchPer100g.group(1)

      priceMatchPer100ml = re.search(r'\$([^$\/]*)\/100ml', product.text)
      if priceMatchPer100ml:
         pricePer100ml = priceMatchPer100ml.group(1)
      
      rows.append([f"{brand} {title}", size, price, salePrice, pricePerUnit, pricePerKg, pricePer100g, pricePer100ml])
      # Write to MongoDB
      collection.insert_one({
         'brand':brand,
         'title': title,
         'size': size,
         'regular_price': price,
         'sale_price': salePrice,
         'price_per_unit': pricePerUnit,
         'price_per_kg': pricePerKg,
         'price_per_100g': pricePer100g,
         'price_per_100ml': pricePer100ml
      })

   with open('superc_scrape.csv', mode='a', newline='', encoding='utf-8') as csvFile: 
      csvWriter = csv.writer(csvFile)
      csvWriter.writerows(rows)
   
   pageNumber += 1

driver.quit()