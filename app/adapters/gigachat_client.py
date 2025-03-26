import logging

import gigachat

from app import config

logger = logging.getLogger(__name__)

SYSTEM_MESSAGE = dict(
    role='system',
    content=(
        'Тебе придет запрос в формате:\nquestion:...\nanswer:...\n'
        'Ты должен ответить на question только с помощью информации содержащейся в answer'
    )
)


async def send_message(question: str, answer: str) -> str:
    logger.info(f'Отправка сообщения в GigaChat')
    message = dict(role='user', content=f'question:{question}\nanswer:{answer}')
    async with gigachat.GigaChat(**config.get_gigachat_creds()) as client:
        response = await client.achat(
            dict(messages=[SYSTEM_MESSAGE, message], max_tokens=3000, temperature=0.5),
        )
        return response.choices[0].message.content
