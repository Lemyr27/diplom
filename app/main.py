from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from app.service_layer import services

app = FastAPI()


class SearchResult(BaseModel):
    filename: str
    text: str


@app.get('/search')
async def search(q: str = '') -> SearchResult:
    result, filename = await services.search(q)
    return SearchResult(filename=filename, text=result)


@app.post('/docs')
async def add_document(file: UploadFile) -> None:
    await services.add_document(file)
