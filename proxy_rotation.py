import requests
from bs4 import BeautifulSoup
import random
import concurrent.futures
import time

#get the list of free proxies
def getProxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text =='elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies
lst = []
def extract(proxy):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        r = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=1)
        lst.append(proxy)
    except requests.ConnectionError as err:
        # print(repr(err))
        pass
    return proxy

proxylist = getProxies()

#check them all with futures super quick
def working_proxies():
    with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(extract, proxylist)

    return lst

# URL GETTER WITH PROXY
def url_getter_wp(url):
    headers = requests.utils.default_headers()
    headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    })

    tries = 0
    connected = False
    while not connected:
        # After 10 failed proxy connects, we will request a new set of proxies and try agaom.
        num = 0
        lst[:] = []
        print(working_proxies())
        proxies = working_proxies()
        while num < 10:
            print(f"Sending request to {url}")
            try:
                proxy = random.choice(proxies)
                response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=5).content
                soup = BeautifulSoup(response, "html.parser")
                print(f"Successfully connected! It took {tries} tries")
                num += 10
                connected = True
            except Exception as e:
                print(e)
                print(f"Try #{tries}: Failed to connect to site. Trying again...")
                print(f"{num}/10 tries left until proxies refresh")
                tries += 1
                num += 1
            time.sleep(random.randint(0, 2))

    return soup




