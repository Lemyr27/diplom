import logging
import os

logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

ELASTIC_URL = 'http://localhost:9200'

GIGACHAT_TOKEN = os.environ.get('GIGACHAT_TOKEN')
GIGACHAT_MODEL = os.environ.get('GIGACHAT_MODEL')
GIGACHAT_SCOPE = os.environ.get('GIGACHAT_SCOPE')

MINIO_BUCKET = os.environ.get('MINIO_BUCKET')

ELASTICSEARCH_INDEX = os.environ.get('ELASTICSEARCH_INDEX')


def get_gigachat_creds() -> dict:
    return dict(
        credentials=GIGACHAT_TOKEN,
        scope=GIGACHAT_SCOPE,
        model=GIGACHAT_MODEL,
        verify_ssl_certs=False,
    )


def get_minio_creds() -> dict:
    return dict(
        endpoint=os.environ.get('MINIO_URL'),
        access_key=os.environ.get('MINIO_ACCESS_KEY'),
        secret_key=os.environ.get('MINIO_SECRET_KEY'),
        secure=False,
    )


def get_postgres_creds() -> str:
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    db_name = os.environ.get('POSTGRES_DB')
    host = os.environ.get('POSTGRES_HOST')
    port = int(os.environ.get('POSTGRES_PORT'))
    return f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'
