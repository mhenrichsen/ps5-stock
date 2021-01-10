import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import json


app = FastAPI()

@app.get("/add-email")
async def add_email(email: str):
    print(email)
    f = open("emails.txt", "a+")
    f.write(email+'\n')
    f.close()

    return JSONResponse({'Res': 'Email added'})




@app.get("/status")
async def status():
    with open("status.json") as json_file:
        data = json.load(json_file)

        return data


app.mount("/", StaticFiles(directory="website", html=True), name="website")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8008)
