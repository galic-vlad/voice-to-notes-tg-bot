from functools import wraps

from telegram.constants import ChatAction
from telegram.helpers import escape_markdown

from tgbot.models import Note

LIST_OF_ADMINS = [12345678, 87654321]

NOTE_MARKDOWN_TEMPLATE = r"""
*{title}*

created: {date}
tags: {tags}

\-\-\-

_{text}_
"""


def markdown_note_formatting(note: Note, markdown_v: int = 2) -> str:
    return NOTE_MARKDOWN_TEMPLATE.format(
        title=escape_markdown(note.title, version=markdown_v),
        date=escape_markdown(
            note.timestamp.strftime("%Y-%m-%d:%M:%S"),
            version=markdown_v,
        ),
        tags=escape_markdown(", ".join(note.tags), version=markdown_v),
        text=escape_markdown(note.text, version=markdown_v),
    )


def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return await func(update, context, *args, **kwargs)

    return wrapped


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context, *args, **kwargs)

        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)
