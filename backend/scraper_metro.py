
import re
from scraper_utils import launch_scraper

def scrape_metro(product, item):
   if product.find('p', attrs={'data-testid': 'product-brand'}):
         item.brand = product.find('p', attrs={'data-testid': 'product-brand'}).text

   item.name = product.find('h3').text.strip().replace("\"", "")
   if product.find('p', attrs={'data-testid': 'product-package-size'}):
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

launch_scraper('https://www.metro.ca/en/online-grocery/search-page-', 'tile-product', 'metro', scrape_metro)
    


           
               


               


           
