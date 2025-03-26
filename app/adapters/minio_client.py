import io
import logging
from datetime import datetime, timezone

from fastapi import UploadFile
from minio import Minio

from app import config

logger = logging.getLogger(__name__)

minio = Minio(**config.get_minio_creds())


async def put_object(file: UploadFile) -> str:
    logger.info(f'Добавление файла {file.filename} в minio.')
    data = io.BytesIO(await file.read())
    now_timestamp = int(datetime.now(timezone.utc).timestamp())
    fullname = f'{now_timestamp}_{file.filename}'
    minio.put_object(config.MINIO_BUCKET, file.filename, data, file.size)
    return fullname
