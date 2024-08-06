import os
from fastapi import FastAPI, Request
from sys import version as python_formatted_version
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
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

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")


@app.get("/api/messages")   # GET  <host>/messages?add=value to add message
async def r_add(request: Request):
    params = request.query_params
    print("try access to messages throught get")
    if 'add' in params:
        message = str(params['add'])
        print(f"api messages get ={message}")
        if len(message) > 300:
            message = message[:300]
        r.lpush('list_messages', str(message))  # insert at list begin
        r.ltrim('list_messages', 0, 50) # save only first x elements

    return {"redis_values": [i.decode("utf-8") for i in r.lrange('list_messages',0,51)] }    

@app.post("/api/messages")   # POST
async def r_post_add(request: Request):
    adding_to_list_messages:bool = 'add' in request.headers
    print(f"try access to messages throught post that {("will" if adding_to_list_messages else "wont (strange)")} added.")
    print(f"header: {request.headers}, url: {request.url}, recieve: {request.recieve}!")
    if adding_to_list_messages:
        form_data = await request.form()
        message = form_data.get('add').replace("\n","  ")
        print(f"api messages post ={message}")
        if len(message) > 300:
            message = message[:300]
        r.lpush('list_messages', str(message))  # insert at list begin
        r.ltrim('list_messages', 0, 50) # save only first x elements
    return {"redis_values": [i.decode("utf-8") for i in r.lrange('list_messages',0,51)] }    


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
