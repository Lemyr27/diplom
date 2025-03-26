import io

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from app.adapters import elasticsearch
from app.service_layer import services

app = FastAPI()


class SearchResult(BaseModel):
    url: str
    text: str


@app.get('/search')
async def search(q: str = '') -> SearchResult:
    result, url = await services.search(q)
    return SearchResult(url=url, text=result)


@app.post('/docs')
async def add_document(file: UploadFile) -> None:
    new_file = io.BytesIO(await file.read())
    await services.add_document(new_file, file.filename)


@app.post('/indices')
async def clean_index() -> None:
    await elasticsearch.delete_index()
    await elasticsearch.create_index()
