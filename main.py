from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request): 
        return templates.TemplateResponse(
        name="index.html", context={"request": request}
)



if __name__== "__main__":
    uvicorn.run("main:app")