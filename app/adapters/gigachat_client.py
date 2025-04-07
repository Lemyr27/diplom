import logging

import gigachat

from app import config

logger = logging.getLogger(__name__)

SYSTEM_MESSAGE = dict(
    role='system',
    content=(
        'Тебе придет запрос в формате:\nquestion:...\nanswer:...\n'
        'Ты должен ответить на question только с помощью информации содержащейся в answer '
        '(их может быть несколько)'
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


async def generate_keywords(questions: list[str]) -> list[str]:
    logger.info(f'Получение ключевых слов GigaChat')
    system_msg = dict(
        role='system',
        content=(
            'Тебе придет запрос содержащий FAQ через запятую, ты должен '
            'предугадать 5 коротких возможных запросов на этой основе '
            'и вывести их строго через точку с запятой без вводных слов, сразу ответ'
        )
    )
    message = dict(role='user', content=', '.join(questions))
    async with gigachat.GigaChat(**config.get_gigachat_creds()) as client:
        response = await client.achat(
            dict(messages=[system_msg, message], max_tokens=3000, temperature=0.5),
        )
        result = response.choices[0].message.content
        return result.split('; ')
