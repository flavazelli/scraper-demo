from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv

with open('maxi_scrape.csv', mode='w', newline='', encoding='utf-8') as csvFile:
   csvWriter = csv.writer(csvFile)
   csvWriter.writerow(['title', 'size', 'regular price', 'sale price', 'size' 'price/unit', 'price/kg', 'price/100g', 'price/100ml'])
   csvFile.close()

pageNumber = 1
driver = webdriver.Chrome()

while True: 
   driver.get(f'https://www.maxi.ca/en/food/c/27985?page={pageNumber}')
   try:
      WebDriverWait(driver, 180).until(
         EC.visibility_of_element_located((By.CLASS_NAME, "chakra-linkbox"))
      )

      pageSource = driver.page_source
      soup = BeautifulSoup(pageSource, 'html.parser')
      products = soup.select(".chakra-linkbox")
      rows = []

      if not products:
         break

      for product in products:
         title = product.find('h3').text.strip().replace("\"", "")
         size = ""
         brand = ""
         price = product.find('div', attrs={'data-testid': 'price-product-tile'}).text
         salePrice = float()
         pricePerKg = float()
         pricePerUnit = float()
         pricePer100g = float()
         pricePer100ml = float()

         if product.find('p', attrs={'data-testid': 'product-brand'}):
            brand = product.find('p', attrs={'data-testid': 'product-brand'}).text
         
         if len(product.find('p', attrs={'data-testid': 'product-package-size'}).text.split(',')) > 1:
            size = product.find('p', attrs={'data-testid': 'product-package-size'}).text.split(',')[0]

         if product.find('span', attrs={'data-testid': 'was-price'}):
            priceReg = re.search(r'\$([^$\/]*)', product.find('span', attrs={'data-testid': 'was-price'}).text)
            if priceReg:
               price = priceReg.group(1)
         
         if product.find('span', attrs={'data-testid': 'sale-price'}):
            salePriceReg = re.search(r'\$([^$\/]*)', product.find('span', attrs={'data-testid': 'sale-price'}).text)
            if salePriceReg:
                salePrice = salePriceReg.group(1)

         priceMatchPerKg = re.search(r'\$([^$\/]*)\/1kg', product.text)
         if priceMatchPerKg:
            pricePerKg = priceMatchPerKg.group(1)
         
         priceMatchPerUnit = re.search(r'\$([^$\/]*)\/1ea', product.text)
         if priceMatchPerUnit:
            pricePerUnit = priceMatchPerUnit.group(1)
         
         priceMatchPer100g = re.search(r'\$([^$\/]*)\/100g', product.text)
         if priceMatchPer100g:
            pricePer100g = priceMatchPer100g.group(1)

         priceMatchPer100ml = re.search(r'\$([^$\/]*)\/100ml', product.text)
         if priceMatchPer100ml:
            pricePer100ml = priceMatchPer100ml.group(1)
         
         rows.append([f"{brand} {title}",size, price, salePrice, pricePerUnit, pricePerKg, pricePer100g, pricePer100ml])

      with open('maxi_scrape.csv', mode='a', newline='', encoding='utf-8') as csvFile: 
         csvWriter = csv.writer(csvFile)
         csvWriter.writerows(rows)
         csvFile.close()
      
      pageNumber = pageNumber + 1
   except: 
      break

driver.quit()


      
         











