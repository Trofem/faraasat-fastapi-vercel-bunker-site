from fastapi import FastAPI
from sys import version as python_formatted_version
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/")
async def root():
    utc = datetime.utcnow()
    return {"time:": format(utc+timedelta(hours=11))}    # make GMT+11


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
