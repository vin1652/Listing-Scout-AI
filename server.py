from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.workflow import ListingWorkflow

app = FastAPI()
templates = Jinja2Templates(directory="templates")
workflow = ListingWorkflow()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    result = workflow.run(query)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "query": query,
        "analysis": result.analysis,
        "listings": result.listings[:5]
    })