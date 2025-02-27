
import json
from curl_cffi import requests
import time
import re
from bs4 import BeautifulSoup
import random

# Send a GET request to the URL
# Read the proxies from the file
with open('valid_proxies.txt', 'r') as file:
   proxies = file.read().splitlines()

   # Choose a random proxy from the list
   proxy = random.choice(proxies)   

   print(f'Using proxy: {proxy}')

   pageNumber = 1
   # Send a GET request to the URL using the chosen proxy
   response = requests.get(f'https://www.metro.ca/en/online-grocery/search-page-{pageNumber}', impersonate=random.choice(["safari", "chrome", "edge", "firefox"]))

   # Parse the HTML content using BeautifulSoup
   soup = BeautifulSoup(response.text, 'html.parser')

   print(soup.prettify())

   while True:
      try:
         print('Page:', pageNumber)
         products = soup.css.select(".tile-product")
         for product in products:
            # for attr in product.attrs:
            #    if "data-" in attr:
            #       print(f"{attr} - {product.attrs[attr]}")
            #       # Print the JSON object

            print("Item: " + product.attrs['data-product-name'] +  ", " + "Price: " + product.css.select('.pricing__secondary-price')[0].text.replace('\n', '').replace(' ', '').strip())
         pageNumber +=1
         time.sleep(random.randint(5, 10));
         response = requests.get(f'https://www.metro.ca/en/online-grocery/search-page-{pageNumber}', impersonate=random.choice(["safari", "chrome", "edge", "firefox"]))

            # Parse the HTML content using BeautifulSoup
         soup = BeautifulSoup(response.text, 'html.parser')
      except:
         break
      
    


           
               


               


           
