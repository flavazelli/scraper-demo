
from bs4 import BeautifulSoup
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from item import Item
from scraper_utils import connect_to_mongodb, setup_webdriver

# Connect to MongoDB
collection = connect_to_mongodb()
driver = setup_webdriver()

pageNumber = 1

while True: 
   driver.get(f'https://www.metro.ca/en/online-grocery/search-page-{pageNumber}')

   WebDriverWait(driver, 180).until(
      EC.visibility_of_element_located((By.CLASS_NAME, "tile-productx"))
   )

   pageSource = driver.page_source
   soup = BeautifulSoup(pageSource, 'html.parser')
   products = soup.select(".tile-product")

   if not products:
      break

   for product in products:
      item = Item('metro')

      item.name = product.attrs['data-product-name'].strip().replace("\"", "")
   
      price = product.find('div', attrs={'data-testid': 'price-product-tile'}).text

      if product.attrs['data-product-brand']:
         item.brand = product.attrs['data-product-brand'].strip().replace("\"", "")
      
      if product.find('span', class_='head__unit-details'):
         item.size = product.find('span', class_='head__unit-details').text

      if product.find('span', attrs={'data-testid': 'was-price'}):
         priceReg = re.search(r'(?<=\$)(\d+(\.\d{1,2})?)', product.find('span', attrs={'data-testid': 'was-price'}).text)
         if priceReg:
            item.regular_price = priceReg.group(1)
      
      if product.find('span', attrs={'data-testid': 'sale-price'}):
         salePriceReg = re.search(r'(?<=\$)(\d+(\.\d{1,2})?)', product.find('span', attrs={'data-testid': 'sale-price'}).text)
         if salePriceReg:
               item.sale_price = salePriceReg.group(1)

      priceMatchPerKg = re.search(r'\$([^$\/]*)\/1kg', product.find('div', class_='pricing__secondary-price').text)
      if priceMatchPerKg:
         item.price_per_kg = priceMatchPerKg.group(1)
      
      priceMatchPerUnit = re.search(r'\$([^$\/]*)\/un.', product.find('div', class_='pricing__secondary-price').text)
      if priceMatchPerUnit:
         item.price_per_unit = priceMatchPerUnit.group(1)
      
      priceMatchPer100g = re.search(r'\$([^$\/]*)\/100g', product.find('div', class_='pricing__secondary-price').text)
      if priceMatchPer100g:
         item.price_per_100g = priceMatchPer100g.group(1)

      priceMatchPer100ml = re.search(r'\$([^$\/]*)\/100ml', product.find('div', class_='pricing__secondary-price').text)
      if priceMatchPer100ml:
         item.price_per_100ml = priceMatchPer100ml.group(1)
   
      collection.insert_one(item.to_mongo_dict())

   pageNumber = pageNumber + 1
 
driver.quit()
    


           
               


               


           
