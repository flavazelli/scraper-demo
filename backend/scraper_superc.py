# This file contains the scraper for the Superc website.
# The scraper will scrape the product name, brand, size, regular price, sale price, price per kg, price per unit, price per 100g, and price per 100ml.
# The scraper will then store the data in the database.
import re
from scraper_utils import launch_scraper

def scrape_superc(product, item):
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

launch_scraper('https://www.superc.ca/en/search-page-', 'tile-product', 'superc', scrape_superc)