import bs4 as bs
import urllib.request
import time
import main as m


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def update(product, stock, time):
    m.request[product]['stock'] = stock
    m.request[product]['time'] = time


while True:
    for product in m.request:
        url = m.request[product]['product_url']
        name = m.request[product]['product_name']
        identifier = m.request[product]['class']
        store = m.request[product]['store']

        req = urllib.request.Request(url, headers=headers)

        source = urllib.request.urlopen(req).read()
        soup = bs.BeautifulSoup(source,'html.parser')
        filtered = soup.find('div', class_=identifier)


        if store == "Elgiganten":
            if filtered is None:
                print("Item available", name, store)
                update(product, True, time.strftime('%H.%M.%S', time.localtime()))
            else:
                print("Item unavailable", name, store)
                update(product, False, time.strftime('%H.%M.%S', time.localtime()))

        elif store == "Bilka":
            if filtered is None:
                print('Item unavailable', name, store)
                update(product, False, time.strftime('%H.%M.%S', time.localtime()))
            else:
                print('Item available', name, store)
                update(product, False, time.strftime('%H.%M.%S', time.localtime()))

        time.sleep(1)