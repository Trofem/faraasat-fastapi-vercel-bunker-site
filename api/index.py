import os
from fastapi import FastAPI, Request
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

@app.get("/r")   # <host>/r?add=value to add
async def r_add(request: Request):
    params = request.query_params
    pop = None
    if 'add' in params:
        r.lpush('list_val', str(params['add']))   # insert at list begin
        r.ltrim('list_val', 0, 6)                 # save only first 7 elements
    return {"redis_values": [i.decode("utf-8") for i in r.lrange('list_val',0,10)] }    


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
