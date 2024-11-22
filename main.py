from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import random
import httpx
from bs4 import BeautifulSoup
from typing import List

app = FastAPI()

# Mounting static files for images and CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 Templates directory
templates = Jinja2Templates(directory="templates")

# Route for the homepage
@app.get("/")
async def index(request: Request): 
    return templates.TemplateResponse("index.html", context={"request": request})

# Function to scrape links from W3Schools
async def find_links() -> List[str]:
    async with httpx.AsyncClient() as client:
        try:
            # Making a GET request asynchronously
            response = await client.get('https://www.w3schools.com/references/index.php')
            response.raise_for_status()  # Raise error for bad responses
        except httpx.RequestError as e:
            # Handle request errors (e.g., network issues)
            print(f"Request error: {e}")
            return []

        html_content = BeautifulSoup(response.text, 'html.parser')
        raw_data = html_content.find_all("a", class_="ga-nav")
        links = []

        for item in raw_data:
            href = item.get("href")
            if href and href != "javascript:void(0);":
                links.append("https://www.w3schools.com" + href)
        return links

# Route for returning a random link
@app.get("/random-link")
async def random_link():
    links = await find_links()  # Using async function for non-blocking call
    if links:
        selected_link = random.choice(links)
        return JSONResponse(content={"link": selected_link})
    else:
        return JSONResponse(content={"error": "Failed to fetch links"}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
