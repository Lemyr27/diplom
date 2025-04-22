import io

from fastapi import FastAPI, UploadFile
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from app import schemas, views
from app.adapters import elasticsearch, orm
from app.service_layer import services

orm.start_mapper()

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/templates')


@app.get('/', tags=['frontend'])
async def homepage(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('chat.html', {'request': request})


@app.post('/chat', tags=['chat'])
async def chat(msg: schemas.MessageBody) -> schemas.SearchResult:
    result = await services.chat(msg.content)
    return schemas.SearchResult(url=result.url, text=result.text, filename=result.filename)


@app.get('/chat', tags=['chat'])
async def get_chat() -> schemas.Chat:
    result = await views.get_chat()
    keywords = await services.generate_keywords()
    result.keywords = keywords
    return result


@app.delete('/chat', tags=['chat'])
async def remove_chat() -> None:
    await services.remove_chat()


@app.post('/docs', tags=['admin'])
async def add_document(file: UploadFile) -> None:
    new_file = io.BytesIO(await file.read())
    await services.add_document(new_file, file.filename)


@app.delete('/indices', tags=['admin'])
async def clean_index() -> None:
    await elasticsearch.delete_index()
    await elasticsearch.create_index()
