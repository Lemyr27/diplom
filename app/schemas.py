from pydantic import BaseModel


class SearchResult(BaseModel):
    url: str
    text: str
    filename: str