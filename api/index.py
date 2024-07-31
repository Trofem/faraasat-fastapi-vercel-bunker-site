import os
from fastapi import FastAPI, Request
from sys import version as python_formatted_version
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
from bunkerGame import CreateRandomCharacter
import redis

app = FastAPI()

directory = os.path.dirname(os.path.abspath(__file__))
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

@app.get("/")
async def root():
    return {
        "GMT+11 time": format(datetime.utcnow()+timedelta(hours=11))
        }    # make GMT+11

@app.get("/r")   # GET  <host>/r?add=value to add
async def r_add(request: Request):
    params = request.query_params
    time_str = format(datetime.utcnow()+timedelta(hours=11))+" GMT+11"
    if 'add' in params:
        r.lpush('list_val', time_str+' (GET) '+str(params['add']))   # insert at list begin
        r.ltrim('list_val', 0, 20)                 # save only first x elements
    return {"redis_values": [i.decode("utf-8") for i in r.lrange('list_val',0,21)] }    

@app.post("/r")   # POST
async def r_post_add(request: Request):
    if 'add' in request.headers:
        time_str = format(datetime.utcnow()+timedelta(hours=11))+" GMT+11"
        add_value = request.headers.get('add')
        r.lpush('list_val', time_str+' (POST) '+str(add_value))         # insert at list begin
        r.ltrim('list_val', 0, 20)                  # save only first x elements
    return {"redis_values": [i.decode("utf-8") for i in r.lrange('list_val',0,21)] }    


@app.get("/character") #GET (already created) random bunker character 
async def root(request: Request): #<host>/character?json
    try:
        isJson = True if 'json' in request.headers else False
        
        if character_output == "Null": #in case if not created
            character_output = CreateRandomCharacter(isJson=False)

        return {
            character_output
            } 
    except Exception as e:

        return {f"getting character is failed.... \n {e}"}


@app.get("/html", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>Hello, user!</title> </head>
        <body><h1>faraasat-fastapi-vercel-example!</h1></body>
    </html> """+'@python '+str(python_formatted_version)
