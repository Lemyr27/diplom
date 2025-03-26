import logging

from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

from app.adapters import docx, elasticsearch, gigachat_client, minio_client

logger = logging.getLogger(__name__)


async def _create_docs_from_text(text: str) -> list[Document]:
    text_splitter = CharacterTextSplitter(separator='.', chunk_size=1024, chunk_overlap=256)
    return text_splitter.create_documents([text])


async def index_document(file: UploadFile, filename: str) -> None:
    text = docx.get_text(await file.read())
    docs = await _create_docs_from_text(text)
    for i, doc in enumerate(docs):
        await elasticsearch.index_document(
            text=doc.page_content,
            filename=filename,
            chunk_id=i,
        )


async def search(question: str) -> tuple[str, str]:
    answer, filename = await elasticsearch.search(question)
    result = await gigachat_client.send_message(question, answer)
    return result, filename


async def add_document(file: UploadFile) -> None:
    filename = await minio_client.put_object(file)
    await index_document(file, filename)

