
import json
from curl_cffi import requests
import time

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
   try:
      response = requests.get('https://www.iga.net/en/online_grocery/browse?page={pageNumber}', impersonate=random.choice(["safari", "chrome", "edge", "firefox"]),proxy=proxy)
   # Parse the HTML content using BeautifulSoup
      soup = BeautifulSoup(response.text, 'html.parser')

      print(soup.prettify())

      while True:
         print('Page:', pageNumber);
         products = soup.css.select(".item-product")
         for product in products:
            if "data-product" in product.attrs:
               # Print the JSON object
               obj = json.loads(product["data-product"].replace("'", "\""))
               print(f"{obj['FullDisplayName']} - ${obj['RegularPrice']}")

         nextPageLink = soup.css.select(".pagination__arrow--right")
         print(nextPageLink);
         if nextPageLink and "is-disabled" not in nextPageLink[0].attrs.get("class", []):
            pageNumber += 1
            time.sleep(random.randint(5, 10))
            response = requests.get('https://www.iga.net/en/online_grocery/browse?page={pageNumber}', impersonate=random.choice(["safari", "chrome", "edge", "firefox"]))
            soup = BeautifulSoup(response.text, 'html.parser')
         else:
            break
   except:
       print(f"Proxy {proxy} not working")
       proxy = random.choice(proxies)  



  


           
               


               


           
