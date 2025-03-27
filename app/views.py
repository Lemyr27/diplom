from app import schemas
from app.service_layer import unit_of_work


async def get_chat(
    uow: unit_of_work.SqlAlchemyUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
) -> schemas.Chat:
    async with uow:
        messages = await uow.messages.list()
        return schemas.Chat(
            messages=[
                schemas.Message(
                    url=msg.url,
                    user_msg=msg.user_msg,
                    bot_msg=msg.bot_msg,
                    filename=msg.filename,
                )
                for msg in messages
            ]
        )
