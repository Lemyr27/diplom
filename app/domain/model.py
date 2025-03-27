from datetime import datetime


class Message:
    created_at: datetime

    def __init__(self, user_msg: str, bot_msg: str, filename: str, url: str):
        self.user_msg = user_msg
        self.bot_msg = bot_msg
        self.filename = filename
        self.url = url
