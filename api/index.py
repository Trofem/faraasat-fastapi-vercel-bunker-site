import os
import json
from sys import version as python_formatted_version
from datetime import datetime, timedelta
import urllib.parse
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
import redis
from .bunkergame import *

app = FastAPI()

site_output = "Null"

KV_USERNAME = os.environ.get('KV_USERNAME')
KV_PASS = os.environ.get('KV_PASS')
KV_HOST = os.environ.get('KV_HOST')
KV_PORT = os.environ.get('KV_PORT')
KV_TELEGRAM_TOKEN = os.environ.get('KV_TELEGRAM_TOKEN')


r = redis.Redis(
    host=KV_HOST,
    port=KV_PORT,
    username=KV_USERNAME, 
    password=KV_PASS,
    ssl=True
)

def get_token() -> str:
    return KV_TELEGRAM_TOKEN

def get_feedbacks() -> str:
    return {"messages" : [i.decode("utf-8") for i in r.lrange('list_message',0,51)]}

#async def get_data() -> str:
    #return json.dumps( {"datetime": datetime.utcnow()+timedelta(hours=11)} )

@app.get("/date")
async def root():
    return json.dumps( {"datetime": datetime.utcnow()+timedelta(hours=11)} )  # make GMT+11

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")


@app.get("/api/messages")   # GET  <host>/messages?add=value to add message
async def r_add(request: Request):
    params = request.query_params
    print("try access to messages throught get")
    if 'add' in params:
        message = params['add']
        print(f"api messages get ={message}")
        if len(message) > 300:
            message = message[:300]
        r.lpush('list_message', f'{message}')  # insert at list begin
        r.ltrim('list_message', 0, 50) # save only first x elements

    return get_feedbacks()  

@app.post("/api/messages")   # POST
async def r_post_add(request: Request):
    adding_to_list_message:bool = 'add' in request.headers
    print(f"try access to messages throught post that {("will" if adding_to_list_message else "wont (strange)")} added.")
    print(f"header: {request.headers}, url: {request.url}!")
    if adding_to_list_message:
        message = urllib.parse.unquote(request.headers['add'])
        message = message.replace("\n", "  ")
        print(f"api messages post ={message}")
        if len(message) > 300:
            message = message[:300]
        r.lpush('list_message', f'user: {request.headers["user-agent"]}, message: {message}')  # insert at list begin
        r.ltrim('list_message', 0, 50) # save only first x elements


@app.get("/api/character") #GET random bunker character 
async def get_character(request: Request): #<host>/api/character?json
    global site_output
    print(f"api character get")
    params = request.query_params
    isJson = 'json' in params
    site_output = CreateRandomCharacter(isJson=isJson)
    return HTMLResponse(site_output) if not isJson else JSONResponse(site_output)


@app.get("/api/bunker") #GET random bunker building
async def get_bunker(request: Request): #<host>/api/bunker?json
    global site_output
    print(f"api bunker get")
    params = request.query_params
    isJson = 'json' in params
    site_output = CreateRandomBunker(isJson=isJson)
    return HTMLResponse(site_output) if not isJson else JSONResponse(site_output)


@app.get("/", response_class=HTMLResponse)
async def main():
    print(f"api website get")
    with open( HTMLdirectory+"mainSite.html", "r" ) as f:
        return f.read()
    
#@python {str(python_formatted_version)}
