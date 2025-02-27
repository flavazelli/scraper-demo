import requests

import concurrent.futures

def validate_proxy(proxy):
    try:
        response = requests.get('https://www.example.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        if response.status_code == 200:
            print(proxy)
            
            return proxy
    except:
        pass

def main():
    proxies = []
    with open('proxies.txt', 'r') as file:
        proxies = file.read().splitlines()

    valid_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(validate_proxy, proxies)
        for result in results:
            if result:
                valid_proxies.append(result)

    for proxy in valid_proxies:
        print(proxy)

if __name__ == '__main__':
    main()
    