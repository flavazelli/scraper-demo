from  langchain_community.document_loaders.url_selenium import SeleniumURLLoader
from typing import List, Union
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from unstructured.partition.html import partition_html
from selenium.webdriver import Chrome, Firefox
from langchain_core.documents import Document
from bs4 import SoupStrainer, BeautifulSoup
from selenium import webdriver
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
import undetected_chromedriver as uc
from dotenv import load_dotenv
import os
load_dotenv()

class SeleniumOverride(SeleniumURLLoader): 

    def __init__(self, *args, proxy, lock, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy = proxy
        self.lock = lock
    
    # Child's show method 
    def load(self, attribute, search_class, product_class) -> List[Document]:
        """Load the specified URLs using Selenium and create Document instances.

        Returns:
            List[Document]: A list of Document instances with loaded content.
        """
       
        docs: List[Document] = list()
        driver = self._get_driver()

        for url in self.urls:
            try:
                driver.get(url)
                if attribute == "class":
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, search_class))
                    )
                
                elif attribute == "attribute":
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='list-view']"))
                    )
                page_content = driver.page_source

                if attribute == "class":
                    soup = BeautifulSoup(page_content, 'html.parser', parse_only=SoupStrainer(
                        class_=product_class
                    ))
                elif attribute == "attribute":
                    soup = BeautifulSoup(page_content, 'html.parser', parse_only=SoupStrainer(
                       "div", attrs={"data-testid": "list-view"}
                    ))
                
                if attribute == "class":
                    products = soup.select(f'.{search_class}')
                elif attribute == "attribute":
                    products = soup.select("div[data-testid='list-view']")

                for product in products:
                    elements = partition_html(text=product.prettify(formatter=None))
                    text = "\n\n".join([str(el) for el in elements])
                    metadata = self._build_metadata(url, driver)
                    docs.append(Document(page_content=text, metadata=metadata))
            except Exception as e:
                if self.continue_on_failure:
                    print(f"Error fetching or processing {url}, exception: {e}")
                else:
                    raise e

        driver.quit()
        return docs
    
    def _get_driver(self) -> Union["Chrome", "Firefox"]:
            """Create and return a WebDriver instance based on the specified browser.

            Raises:
                ValueError: If an invalid browser is specified.

            Returns:
                Union[Chrome, Firefox]: A WebDriver instance for the specified browser.
            """
            if self.browser.lower() == "chrome":
                from selenium.webdriver import Chrome
                from selenium.webdriver.chrome.options import Options as ChromeOptions
                from selenium.webdriver.chrome.service import Service

                chrome_options = ChromeOptions()

                with self.lock:
                    if os.getenv('USE_PROXY', 'False') == 'True'and os.getenv('PROXY_URL') is not None:
                        print('proxy true')
                        username = os.getenv('PROXY_USERNAME')
                        password = os.getenv('PROXY_PASSWORD')
                        endpoint = os.getenv('PROXY_URL')
                        port = os.getenv('PROXY_PORT')
                        # Initialize SeleniumAuthenticatedProxy
                        proxy_helper = SeleniumAuthenticatedProxy(proxy_url=f"https://{username}:{password}@{endpoint}:{port}")
                        # Enrich Chrome options with proxy authentication
                        proxy_helper.enrich_chrome_options(chrome_options) 

                    elif os.getenv('USE_PROXY') and os.getenv('PROXY_URL') is None:
                        #TODO return validate proxies
                        pass

                    for arg in self.arguments:
                        chrome_options.add_argument(arg)

                    if self.headless:
                        chrome_options.add_argument("--headless")
                        chrome_options.add_argument("--no-sandbox")
                    if self.binary_location is not None:
                        chrome_options.binary_location = self.binary_location
                    if self.executable_path is None:
                        return uc.Chrome(options=chrome_options)
                    return uc.Chrome(  
                        options=chrome_options,
                        service=Service(executable_path=self.executable_path),
                    )
            elif self.browser.lower() == "firefox":
                from selenium.webdriver import Firefox
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                from selenium.webdriver.firefox.service import Service

                firefox_options = FirefoxOptions()

                for arg in self.arguments:
                    firefox_options.add_argument(arg)

                if self.headless:
                    firefox_options.add_argument("--headless")
                if self.binary_location is not None:
                    firefox_options.binary_location = self.binary_location
                if self.executable_path is None:
                    return Firefox(options=firefox_options)
                return Firefox(
                    options=firefox_options,
                    service=Service(executable_path=self.executable_path),
                )
            else:
                raise ValueError("Invalid browser specified. Use 'chrome' or 'firefox'.")