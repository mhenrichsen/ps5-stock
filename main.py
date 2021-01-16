import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from threading import Timer
import re
import requests as r
import json
import os

app = FastAPI()
FILE_NAME = "emails.txt"
# regular expression for validating the Email
EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
MAX_REQUEST = 3  # Before timeout
DEQUE_TIME = 60  # Seconds
host_dict = {}

database_ip = os.environ['database']
database_url = 'http://'+database_ip+'/direct-call'
get_products = 'http://'+database_ip+'/get-all-products'


@app.get("/add-email")
async def add_email(email: str, request: Request):
    print(host_dict)
    if request.client.host in host_dict:
        if host_dict.get(request.client.host) < MAX_REQUEST:
            host_dict[request.client.host] += 1
            # Check if email is valid
            if re.search(EMAIL_REGEX, email):
                print(email + ' ready to be added')
                params = {'call_type': "duplicate_check", "email": email}
                res = r.get(url=database_url, params=params)
                json_res = res.json()['res']
                print(json_res)
                if json_res == 'Email added':
                    return JSONResponse({'Res': json_res})
                else:
                    return JSONResponse({'Res': json_res})
        print('Invalid email')
        return JSONResponse({'Res': 'Invalid email'}, 400)
    else:
        host_dict[request.client.host] = 0
        return await add_email(email, request)


@app.get("/remove-email")
async def remove_email(email: str):
    params = {'call_type': "remove-email", "email": email}
    res = r.get(url=database_url, params=params)

    if res.status_code == 200:
        return HTMLResponse(
            """
            <html>
                <head>
                    <title>Email fjernet</title>
                </head>
                <body>
                    <h1>""" + email + """ blev fjernet fra listen</h1>
                </body>
            </html>
            """)
    else:
        return HTMLResponse('Something went wrong')


# Save email to file

@app.get("/status")
async def status():
    data = r.get(get_products).json()
    data = json.loads(data)
    return data


# Repeat function call with set timer
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def deque_hosts():
    to_remove = []
    for host in host_dict:
        if host_dict.get(host) == 0:
            to_remove.append(host)
        else:
            host_dict[host] -= 1
    for host in to_remove:
        host_dict.pop(host)


# deque requests from dictionary slowly to avoid spam
timer = RepeatTimer(DEQUE_TIME, deque_hosts)
timer.start()

app.mount("/", StaticFiles(directory="website", html=True), name="website")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
