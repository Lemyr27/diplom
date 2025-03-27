from pydantic import BaseModel


class SearchResult(BaseModel):
    url: str
    text: str
    filename: str


class MessageBody(BaseModel):
    content: str


class Message(BaseModel):
    user_msg: str
    bot_msg: str
    filename: str
    url: str


class Chat(BaseModel):
    messages: list[Message]
