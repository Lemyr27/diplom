import logging
from dataclasses import dataclass

from elasticsearch import AsyncElasticsearch

from app import config
from app.adapters import embedding

logger = logging.getLogger(__name__)


async def create_index() -> None:
    async with AsyncElasticsearch(config.ELASTIC_URL) as es_client:
        index = config.ELASTICSEARCH_INDEX
        logger.debug(f'Создаем индекс {index}.')
        props = {
            'text': {'type': 'text'},
            'filename': {'type': 'keyword'},
            'chunk_id': {'type': 'integer'},
            'text_embedding': {
                'type': 'dense_vector',
                'dims': 512,
                'index': True,
                'similarity': 'cosine'
            }
        }
        await es_client.indices.create(index=index, mappings={'properties': props})


async def index_document(text: str, filename: str, chunk_id: int) -> None:
    document = dict(text=text, filename=filename, chunk_id=chunk_id)
    document['text_embedding'] = embedding.get_embedding(text)
    async with AsyncElasticsearch(config.ELASTIC_URL) as es_client:
        logger.debug(f'В индекс {config.ELASTICSEARCH_INDEX} помещаем документ {document}.')
        await es_client.index(index=config.ELASTICSEARCH_INDEX, document=document)


async def delete_index() -> None:
    async with AsyncElasticsearch(config.ELASTIC_URL) as es_client:
        index = config.ELASTICSEARCH_INDEX
        if await es_client.indices.exists(index=index):
            logger.debug(f'Удаляем индекс {index}.')
            await es_client.indices.delete(index=index)


@dataclass
class Search:
    text: str
    filename: str


async def search(query: str) -> list[Search]:
    async with AsyncElasticsearch(config.ELASTIC_URL) as es_client:
        query_embedding = embedding.get_embedding(query)
        lexical_search = {'match': {'text': {'query': query, 'boost': 0.5}}}
        semantic_search = {
            'script_score': {
                'query': {'match_all': {}},
                'script': {
                    'source': 'cosineSimilarity(params.query_vector, "text_embedding") + 1.0',
                    'params': {'query_vector': query_embedding}
                }
            }
        }
        search_query = {
            'query': {'bool': {'must': [lexical_search], 'should': [semantic_search]}},
            'size': 2,
        }
        response = await es_client.search(index=config.ELASTICSEARCH_INDEX, body=search_query)
        hits = response['hits']['hits']

        results: list[Search] = []
        for s in hits:
            res = Search(text=s['_source']['text'], filename=s['_source']['filename'])
            results.append(res)

        return results
