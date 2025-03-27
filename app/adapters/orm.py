import logging

from sqlalchemy import Table, Column, Integer, TIMESTAMP, func, Text
from sqlalchemy.orm import registry

from app.domain import model

logger = logging.getLogger(__name__)

mapper_registry = registry()

messages = Table(
    'messages',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_msg', Text, nullable=False),
    Column('bot_msg', Text, nullable=False),
    Column('url', Text, nullable=False),
    Column('filename', Text, nullable=False),
    Column('created_at', TIMESTAMP(True), server_default=func.now(), nullable=False),
)


def start_mapper() -> None:
    logger.debug('Запуск маппинга таблиц и моделей.')
    mapper_registry.map_imperatively(model.Message, messages)
