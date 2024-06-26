from fastapi import FastAPI
from sys import version as python_formatted_version
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


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
