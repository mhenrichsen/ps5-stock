import bs4 as bs
import urllib.request
import time
import json
import mail as m
import requests as r
import os

database_ip = os.environ['database']
get_products = 'http://'+database_ip+'/get-all-products'
update_product = 'http://'+database_ip+'/update-product'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def update(url, stock, time):
    params = {'url': url, 'stock': stock, 'time': time}
    r.get(url=update_product, params=params)


def filter_html(url, find, identifier):
    req = urllib.request.Request(url, headers=headers)
    source = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(source, 'html.parser')

    return soup.find(find, class_=identifier)


while True:
    in_stock = []
    data = r.get(get_products).json()
    data = json.loads(data)
    for product in data:
        try:
            product_url = product['product_url']
            name = product['product_name']
            identifier = product['class']
            store = product['store']
            find = product['find']

            filtered = filter_html(product_url, find, identifier)

            if store == "Elgiganten" or store == "Proshop" or store == "Happii" or store == "Merlin":
                if filtered is None:
                    print("Item available", name, store)
                    update(product_url, "På lager", time.strftime('%H:%M:%S', time.localtime()))
                    in_stock.append({'store': store, 'name': name, 'url': product_url})
                else:
                    print("Item unavailable", name, store)
                    update(product_url, "Ikke på lager", time.strftime('%H:%M:%S', time.localtime()))

            elif store == "Bilka" or store == "Coolshop" or store == "Power" or store == "Foetex" or store == "BR" or store == "Expert":
                if filtered is None:
                    print('Item unavailable', name, store)
                    update(product_url, "Ikke på lager", time.strftime('%H:%M:%S', time.localtime()))
                else:
                    print('Item available', name, store)
                    update(product_url, "På lager", time.strftime('%H:%M:%S', time.localtime()))
                    in_stock.append({'store': store, 'name': name, 'url': product_url})

            time.sleep(1)
        except Exception as e:
            print(e)
    if len(in_stock) > 0:
        print('Lets email!')
        m.send_email(in_stock)
