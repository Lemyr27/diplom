import io

from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

from app import schemas
from app.adapters import elasticsearch, gigachat_client, minio_client, docx


async def _create_docs_from_text(text: str) -> list[Document]:
    text_splitter = CharacterTextSplitter(separator='.', chunk_size=512, chunk_overlap=256)
    return text_splitter.create_documents([text])


async def index_document(file: io.BytesIO, filename: str) -> None:
    text = docx.get_text_from_docx(file)
    docs = await _create_docs_from_text(text)
    for i, doc in enumerate(docs):
        await elasticsearch.index_document(text=doc.page_content, filename=filename, chunk_id=i)


async def search(question: str) -> schemas.SearchResult:
    search_results = await elasticsearch.search(question)
    avg_answer = '\nanswer:'.join(r.text for r in search_results)
    url = await minio_client.get_object_url(search_results[0].filename)
    result = await gigachat_client.send_message(question, avg_answer)
    return schemas.SearchResult(text=result, url=url, filename=search_results[0].filename[11:])


async def add_document(file: io.BytesIO, filename: str) -> None:
    fullname = await minio_client.put_object(file, filename)
    try:
        await index_document(file, fullname)
    except:
        await minio_client.remove_object(fullname)
        raise
