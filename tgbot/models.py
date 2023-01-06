import datetime
from typing import Optional

import attrs
import pydantic
from aiogram.types import Message


@attrs.define
class DeepgramResponse:
    text: str
    summary: str


class Note(pydantic.BaseModel):
    language: str
    timestamp: datetime.datetime
    text: str
    tags: list[str]
    summary: str
    title: str
    origin_voice_msg_id: int
    chat_id: int
    user_id: int
    exported: bool


@attrs.define
class ConversationStorage:
    voice_msg: Optional[Message] = None
    note: Optional[Note] = None
