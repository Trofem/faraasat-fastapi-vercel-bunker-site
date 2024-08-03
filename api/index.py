import os
from fastapi import FastAPI, Request
from sys import version as python_formatted_version
from fastapi.responses import HTMLResponse, JSONResponce
from datetime import datetime, timedelta
from .bunkergame import *
import redis

app = FastAPI()

site_output = "Null"

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

@app.get("/date")
async def root():
    return {
        "GMT+11 time": format(datetime.utcnow()+timedelta(hours=11))
        }    # make GMT+11

@app.get("/messages")   # GET  <host>/messages?add=value to add message
async def r_add(request: Request):
    params = request.query_params

    if 'add' in params:
        message = str(params['add']).replace("\n"," ")

        if len(message) > 200:
            message = message[:200]
        r.lpush(str(message))  # insert at list begin
        r.ltrim('list_messages', 0, 50) # save only first x elements

    return {"redis_values": [i.decode("utf-8") for i in r.lrange('list_messages',0,51)] }    

@app.post("/messages")   # POST
async def r_post_add(request: Request):

    if 'add' in request.headers:

        message = request.headers.get('add')

        if len(message) > 200:
            message = message[:200]
        r.lpush(str(message))  # insert at list begin
        r.ltrim('list_messages', 0, 50) # save only first x elements

    return {"redis_values": [i.decode("utf-8") for i in r.lrange('list_messages',0,51)] }    


@app.get("/api/character") #GET (already created) random bunker character 
async def get_character(request: Request): #<host>/api/character?json
    global site_output
    params = request.query_params
    isJson = 'json' in params
    site_output = CreateRandomCharacter(isJson=isJson)
    return HTMLResponse(site_output) if not isJson else JSONResponse(site_output)


@app.get("/api/bunker") #GET (already created) random bunker building
async def get_bunker(request: Request): #<host>/api/bunker?json
    global site_output
    params = request.query_params
    isJson = 'json' in params
    site_output = CreateRandomBunker(isJson=isJson)
    return HTMLResponse(site_output) if not isJson else JSONResponse(site_output)


@app.get("/", response_class=HTMLResponse)
async def main():
    with open( HTMLdirectory+"mainSite.html", "r" ) as f:
        return f.read()
    
#@python {str(python_formatted_version)}
