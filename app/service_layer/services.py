import io

from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from sqlalchemy import text

from app import schemas
from app.adapters import elasticsearch, gigachat_client, minio_client, docx
from app.domain import model
from app.service_layer import unit_of_work


async def _create_docs_from_text(text: str) -> list[Document]:
    text_splitter = CharacterTextSplitter(separator='.', chunk_size=512, chunk_overlap=256)
    return text_splitter.create_documents([text])


async def index_document(file: io.BytesIO, filename: str) -> None:
    text = docx.get_text_from_docx(file)
    docs = await _create_docs_from_text(text)
    for i, doc in enumerate(docs):
        await elasticsearch.index_document(text=doc.page_content, filename=filename, chunk_id=i)


async def chat(
    question: str,
    uow: unit_of_work.SqlAlchemyUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
) -> schemas.SearchResult:
    async with uow:
        search_results = await elasticsearch.search(question)
        avg_answer = '\nanswer:'.join(r.text for r in search_results)
        url = await minio_client.get_object_url(search_results[0].filename)
        result = await gigachat_client.send_message(question, avg_answer)

        filename = search_results[0].filename[11:]
        message = model.Message(user_msg=question, bot_msg=result, filename=filename, url=url)
        await uow.messages.add(message)
        await uow.commit()

        return schemas.SearchResult(text=result, url=url, filename=filename)


async def remove_chat(
    uow: unit_of_work.SqlAlchemyUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
) -> None:
    async with uow:
        await uow.session.execute(text('DELETE FROM messages'))
        await uow.commit()


async def add_document(file: io.BytesIO, filename: str) -> None:
    fullname = await minio_client.put_object(file, filename)
    try:
        await index_document(file, fullname)
    except:
        await minio_client.remove_object(fullname)
        raise


async def generate_keywords(
    uow: unit_of_work.SqlAlchemyUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
) -> list[str]:
    async with uow:
        stmt = 'SELECT user_msg FROM messages'
        result = await uow.session.execute(text(stmt))
        messages = list(result.scalars().all())
        keywords = await gigachat_client.generate_keywords(messages)
        return keywords
