import requests
from concurrent.futures import ThreadPoolExecutor

def fetch_proxies():
    url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=ca&protocol=http&proxy_format=protocolipport&format=text&timeout=20000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip().split("\r\n")
    except requests.RequestException as e:
        print(f"An error occurred while fetching proxies: {e}")
        return []

def is_proxy_valid(proxy):
    test_url = "http://httpbin.org/ip"
    try:
        response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def validate():
    proxies = fetch_proxies()
    valid_proxies = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(is_proxy_valid, proxies)
        valid_proxies = [proxy for proxy, valid in zip(proxies, results) if valid]
    return valid_proxies
