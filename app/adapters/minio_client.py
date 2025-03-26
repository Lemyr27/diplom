import io
import logging
from datetime import datetime, timezone

from fastapi import UploadFile
from minio import Minio

from app import config

logger = logging.getLogger(__name__)

minio = Minio(**config.get_minio_creds())


async def put_object(file: io.BytesIO, filename: str) -> str:
    logger.info(f'Добавление файла {filename} в minio.')
    now_timestamp = int(datetime.now(timezone.utc).timestamp())
    fullname = f'{now_timestamp}_{filename}'
    minio.put_object(config.MINIO_BUCKET, fullname, file, file.getbuffer().nbytes)
    return fullname


async def get_object_url(filename: str) -> str:
    return minio.get_presigned_url('GET', config.MINIO_BUCKET, filename)


async def remove_object(filename: str) -> None:
    logger.info(f'Удаление файла {filename} из minio.')
    minio.remove_object(config.MINIO_BUCKET, filename)
