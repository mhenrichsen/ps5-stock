import bs4 as bs
import urllib.request
import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def update(product, stock, time, data):
    with open('status.json', 'w') as outfile:
        data[product]['stock'] = stock
        data[product]['time'] = time

        json.dump(data, outfile)


while True:
    with open('status.json') as json_file:
        data = json.load(json_file)
    for product in data:
        url = data[product]['product_url']
        name = data[product]['product_name']
        identifier = data[product]['class']
        store = data[product]['store']
        find = data[product]['find']

        req = urllib.request.Request(url, headers=headers)

        source = urllib.request.urlopen(req).read()
        soup = bs.BeautifulSoup(source, 'html.parser')
        filtered = soup.find(find, class_=identifier)

        if store == "Elgiganten" or store == "Proshop":
            if filtered is None:
                print("Item available", name, store)
                update(product, "På lager", time.strftime('%H.%M.%S', time.localtime()), data)
            else:
                print("Item unavailable", name, store)
                update(product, "Ikke på lager", time.strftime('%H.%M.%S', time.localtime()), data)

        elif store == "Bilka":
            if filtered is None:
                print('Item unavailable', name, store)
                update(product, "Ikke på lager", time.strftime('%H.%M.%S', time.localtime()), data)
            else:
                print('Item available', name, store)
                update(product, "På lager", time.strftime('%H.%M.%S', time.localtime()), data)

        time.sleep(1)
