import bs4 as bs
import urllib.request
import time

request = {'product1': {'product_url': 'https://www.elgiganten.dk/product/gaming/konsoller/playstation-konsoller/220280/playstation-5-ps5-digital-edition', 'product_name': 'Digital', 'class': 'not-available'},
           'product2': {'product_url': 'https://www.elgiganten.dk/product/gaming/konsoller/playstation-konsoller/220276/playstation-5-ps5','product_name': 'Disc Standard', 'class': 'not-available'},
           'product3': {'product_url': 'https://www.bilka.dk/produkter/sony-playstation-5/100532624/','product_name': 'Disc Standard', 'class': 'purchase-button v-btn v-btn--block v-btn--contained theme--light v-size--large secondary mt-5 flex-grow-0'}}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


while True:
    for product in request:
        url = request[product]['product_url']
        name = request[product]['product_name']
        identifier = request[product]['class']

        req = urllib.request.Request(url, headers=headers)

        source = urllib.request.urlopen(req).read()
        soup = bs.BeautifulSoup(source,'lxml')
        filtered = soup.find('div', class_=identifier)


        if filtered is None:
            print("Item available", name)
        else:
            print("Item unavailable", name)

        time.sleep(3)

