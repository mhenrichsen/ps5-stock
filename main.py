import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from threading import Timer
import re
import json

app = FastAPI()
FILE_NAME = "emails.txt"
# regular expression for validating the Email
EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
MAX_REQUEST = 3  # Before timeout
DEQUE_TIME = 60  # Seconds
host_dict = {}


@app.get("/add-email")
async def add_email(email: str, request: Request):
    print(host_dict)
    if request.client.host in host_dict:
        if host_dict.get(request.client.host) < MAX_REQUEST:
            host_dict[request.client.host] += 1
            # Check if email is valid
            if re.search(EMAIL_REGEX, email):
                if await save_email(email):
                    return JSONResponse({'Res': 'Email added'})
        return JSONResponse({'Res': 'Invalid email'}, 400)
    else:
        host_dict[request.client.host] = 0
        return await add_email(email, request)


@app.get("/remove-email")
async def remove_email(email: str, request: Request):
    with open("emails.txt", "r") as f:
        lines = f.readlines()
    with open("emails.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != email:
                f.write(line)

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


# Save email to file
async def save_email(email: str):
    if not file_contains_string(FILE_NAME, email):
        print("Saving: " + email)
        f = open(FILE_NAME, "a+")
        f.write(email + '\n')
        f.close()
        return True
    else:
        print("Email was duplicate: " + email)
        return False


@app.get("/status")
async def status():
    with open("status.json") as json_file:
        data = json.load(json_file)

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


def file_contains_string(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False


# deque requests from dictionary slowly to avoid spam
timer = RepeatTimer(DEQUE_TIME, deque_hosts)
timer.start()

app.mount("/", StaticFiles(directory="website", html=True), name="website")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
