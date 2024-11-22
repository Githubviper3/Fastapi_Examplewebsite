from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import requests
import random
from bs4 import BeautifulSoup

app = FastAPI()

# Mounting static files for images and CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 Templates directory
templates = Jinja2Templates(directory="templates")

# Route for the homepage
@app.get("/")
def index(request: Request): 
    return templates.TemplateResponse(
        "index.html", context={"request": request}
    )

# Function to scrape links from W3Schools
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

# Route for returning a random link
@app.get("/random-link")
def random_link():
    links = find_links()
    selected_link = random.choice(links)
    return JSONResponse(content={"link": selected_link})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
