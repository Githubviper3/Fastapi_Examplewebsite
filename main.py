from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import requests
import random
from bs4 import BeautifulSoup

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request): 
        return templates.TemplateResponse(
        name="index.html", context={"request": request}
)

def find_links():
    # Making a GET request
    r = requests.get('https://www.w3schools.com/references/index.php')
    # Parsing the HTML
    html_content = BeautifulSoup(r.content, 'html.parser')
    raw_data = html_content.find_all("a", class_="ga-nav")
    output = []
    for item in raw_data:
        href = item.get("href")
        if href != "javascript:void(0);":
            output.append("https://www.w3schools.com" + href)
    return output
links = find_links()
@app.get("/random-link")
def random_link():
    selected_link = random.choice(links)
    return JSONResponse(content={"link": selected_link})


if __name__== "__main__":
    uvicorn.run("main:app")