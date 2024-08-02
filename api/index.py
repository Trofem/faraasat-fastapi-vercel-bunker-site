import os
from fastapi import FastAPI, Request
from sys import version as python_formatted_version
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
from .bunkergame import CreateRandomCharacter
import redis

app = FastAPI()

HTMLdirectory:str = os.path.abspath(os.getcwd()) + "/html/"
character_output = "Null"

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

@app.get("/d")
async def root():
    return {
        "GMT+11 time": format(datetime.utcnow()+timedelta(hours=11))
        }    # make GMT+11

@app.get("/messages")   # GET  <host>/messages?add=value to add
async def r_add(request: Request):
    params = request.query_params
    time_str = format(datetime.utcnow()+timedelta(hours=11))+" GMT+11"
    if 'add' in params:
        value = str(params['add']).replace("\n"," ")
        if len(value) > 200:
            value = value[:200]
        r.lpush('list_messages', value)   # insert at list begin
        r.ltrim('list_messages', 0, 50)                 # save only first x elements
        print(f"added {value}")
    return {"redis_values": [i.decode("utf-8") for i in r.lrange('list_messages',0,21)] }    

@app.post("/messages")   # POST
async def r_post_add(request: Request):
    if 'add' in request.headers:
        time_str = format(datetime.utcnow()+timedelta(hours=11))+" GMT+11"
        add_value = request.headers.get('add')
        r.lpush('list_val', time_str+' (POST) '+str(add_value))         # insert at list begin
        r.ltrim('list_val', 0, 20)                  # save only first x elements
    return {"redis_values": [i.decode("utf-8") for i in r.lrange('list_val',0,21)] }    


@app.get("/api/character") #GET (already created) random bunker character 
async def get_character(request: Request): #<host>/api/character?json
    global character_output
    params = request.query_params
    isJson = 'json' in params
    character_output = CreateRandomCharacter(isJson=isJson)
    return HTMLResponse(character_output) if not isJson else JSONResponse(character_output)


@app.get("/", response_class=HTMLResponse)
async def main():
    with open( HTMLdirectory+"mainSite.html", "r" ) as f:
        return f.read()
    

#@python {str(python_formatted_version)}
