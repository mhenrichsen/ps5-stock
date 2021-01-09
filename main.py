import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


request = {'product1': {'product_url': 'https://www.elgiganten.dk/product/gaming/konsoller/playstation-konsoller/220280/playstation-5-ps5-digital-edition', 'product_name': 'Digital', 'class': 'not-available', 'store': 'Elgiganten', 'stock': False, 'time': False},
           'product2': {'product_url': 'https://www.elgiganten.dk/product/gaming/konsoller/playstation-konsoller/220276/playstation-5-ps5','product_name': 'Disc Standard', 'class': 'not-available', 'store': 'Elgiganten', 'stock': False, 'time': False},
           'product3': {'product_url': 'https://www.bilka.dk/produkter/sony-playstation-5/100532624/','product_name': 'Disc Standard', 'class': 'purchase-button v-btn v-btn--block v-btn--contained v-btn--disabled theme--light v-size--large mt-5 flex-grow-0', 'store': 'Bilka', 'stock': False, 'time': False},
           'product3': {'product_url': 'https://www.bilka.dk/produkter/sony-playstation-5-digital/100553322/','product_name': 'Digital', 'class': 'purchase-button v-btn v-btn--block v-btn--contained v-btn--disabled theme--light v-size--large mt-5 flex-grow-0', 'store': 'Bilka', 'stock': False, 'time': False},
           }



app = FastAPI()


@app.post("/add-email")
async def add_email():

    return JSONResponse({'hello': 'world'})




@app.get("/status")
async def status():

    return request


app.mount("/", StaticFiles(directory="website", html=True), name="website")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8008)