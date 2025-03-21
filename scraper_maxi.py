from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import re
from item import Item
from scraper_utils import connect_to_mongodb, setup_webdriver

# Connect to MongoDB
collection = connect_to_mongodb()
driver = setup_webdriver()

pageNumber = 1

while True: 
   driver.get(f'https://www.maxi.ca/en/food/c/27985?page={pageNumber}')

   WebDriverWait(driver, 180).until(
      EC.visibility_of_element_located((By.CLASS_NAME, "chakra-linkbox"))
   )

   pageSource = driver.page_source
   soup = BeautifulSoup(pageSource, 'html.parser')
   products = soup.select(".chakra-linkbox")

   if not products:
      break

   for product in products:
      item = Item('maxi')
      item.name = product.find('h3').text.strip().replace("\"", "")
   
      price = product.find('div', attrs={'data-testid': 'price-product-tile'}).text


      if product.find('p', attrs={'data-testid': 'product-brand'}):
         item.brand = product.find('p', attrs={'data-testid': 'product-brand'}).text
      
      if len(product.find('p', attrs={'data-testid': 'product-package-size'}).text.split(',')) > 1:
         item.size = product.find('p', attrs={'data-testid': 'product-package-size'}).text.split(',')[0]

      if product.find('span', attrs={'data-testid': 'was-price'}):
         priceReg = re.search(r'(?<=\$)(\d+(\.\d{1,2})?)', product.find('span', attrs={'data-testid': 'was-price'}).text)
         if priceReg:
            item.regular_price = priceReg.group(1)
      
      if product.find('span', attrs={'data-testid': 'sale-price'}):
         salePriceReg = re.search(r'(?<=\$)(\d+(\.\d{1,2})?)', product.find('span', attrs={'data-testid': 'sale-price'}).text)
         if salePriceReg:
               item.sale_price = salePriceReg.group(1)

      priceMatchPerKg = re.search(r'\$([^$\/]*)\/1kg', product.text)
      if priceMatchPerKg:
         item.price_per_kg = priceMatchPerKg.group(1)
      
      priceMatchPerUnit = re.search(r'\$([^$\/]*)\/1ea', product.text)
      if priceMatchPerUnit:
         item.price_per_unit = priceMatchPerUnit.group(1)
      
      priceMatchPer100g = re.search(r'\$([^$\/]*)\/100g', product.text)
      if priceMatchPer100g:
         item.price_per_100g = priceMatchPer100g.group(1)

      priceMatchPer100ml = re.search(r'\$([^$\/]*)\/100ml', product.text)
      if priceMatchPer100ml:
         item.price_per_100ml = priceMatchPer100ml.group(1)
   
      collection.insert_one(item.to_mongo_dict())

   pageNumber = pageNumber + 1
 
driver.quit()


      
         











