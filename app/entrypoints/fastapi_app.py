import io

from fastapi import FastAPI, UploadFile
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from app import schemas
from app.adapters import elasticsearch
from app.service_layer import services

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/templates')


@app.get('/')
async def homepage(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('chat.html', {'request': request})


@app.get('/search')
async def search(q: str = '') -> schemas.SearchResult:
    result = await services.search(q)
    return schemas.SearchResult(url=result.url, text=result.text, filename=result.filename)


@app.post('/docs')
async def add_document(file: UploadFile) -> None:
    new_file = io.BytesIO(await file.read())
    await services.add_document(new_file, file.filename)


@app.post('/indices')
async def clean_index() -> None:
    await elasticsearch.delete_index()
    await elasticsearch.create_index()
