import os
from fastapi import FastAPI
from sys import version as python_formatted_version
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
import redis

app = FastAPI()

KV_USERNAME = os.environ.get('KV_USERNAME')
KV_PASS = os.environ.get('KV_PASS')
KV_HOST = os.environ.get('KV_HOST')
KV_PORT = os.environ.get('KV_PORT')

r = redis.Redis(
    host=KV_HOST,
    port=KV_PORT,
    username=KV_USERNAME, 
    password=KV_PASS,
    ssl=True
)

@app.get("/")
async def root():
    utc = datetime.utcnow()
    return {"GMT+11 time": format(utc+timedelta(hours=11))}    # make GMT+11

@app.get("/r")
async def root():
    return {"redis_ping": [i.decode("utf-8") for i in r.smembers('mylist')] }    


@app.get("/html", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look me! HTMLResponse!</h1>
        </body>
    </html> """+'@python '+str(python_formatted_version)
