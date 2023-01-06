import enum
import logging

import deepgram
from telegram import ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

import tgbot.settings as settings
from tgbot.models import ConversationStorage, Note
from tgbot.storage import save_note
from tgbot.utils import markdown_note_formatting, send_typing_action
from tgbot.voice_to_text import parse_voice_message

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


class BotStates(enum.IntEnum):
    Finish = ConversationHandler.END
    Cancel = ConversationHandler.END
    Timeout = ConversationHandler.TIMEOUT
    VoiceReceivedActionRequested = 1
    VoiceIsParsed = 2
    NoteIsSent = 3


def init_conversation_storage(chat_data):
    chat_data["conversation_storage"] = ConversationStorage()


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!",
    )


async def voice_is_received_callback(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
) -> BotStates:
    keyboard = [["/parse", "/cancel"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
    )

    init_conversation_storage(context.chat_data)
    context.chat_data["conversation_storage"].voice_msg = update.message

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Select an action",
        reply_markup=reply_markup,
    )

    return BotStates.VoiceReceivedActionRequested


@send_typing_action
async def parse_voice_callback(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
) -> BotStates:
    conversation_storage = context.chat_data["conversation_storage"]

    voice_msg = conversation_storage.voice_msg
    voice_file = await voice_msg.voice.get_file()

    deepgram_client = deepgram.Deepgram(settings.DEEPGRAM_API_TOKEN)

    message_transcription = await parse_voice_message(
        deepgram_client,
        voice_file.file_path,
    )
    note = Note(
        language="en",
        timestamp=conversation_storage.voice_msg.date,
        text=message_transcription.text,
        summary=message_transcription.summary,
        tags=[],
        title=message_transcription.summary,
        origin_voice_msg_id=conversation_storage.voice_msg.message_id,
        chat_id=update.effective_chat.id,
        user_id=update.effective_user.id,
        exported=False,
    )
    conversation_storage.note = note

    reply_markup = ReplyKeyboardMarkup(
        [["/save", "/cancel"]],
        one_time_keyboard=True,
        resize_keyboard=True,
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Your voice message is parsed:"
             f"{message_transcription.text}",
        reply_markup=reply_markup,
    )

    return BotStates.VoiceIsParsed


async def save_note_callback(
        update: Update, context:
        ContextTypes.DEFAULT_TYPE,
) -> BotStates:
    conversation_storage = context.chat_data["conversation_storage"]

    success = save_note(conversation_storage.note)

    if success:
        conversation_storage.note.exported = True

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Your voice message is parsed and saved:",
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{markdown_note_formatting(conversation_storage.note)}",
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    # Clean conversation_storage

    return BotStates.Finish


async def cancel_callback(
    update: Update, context:
    ContextTypes.DEFAULT_TYPE,
) -> BotStates:
    return BotStates.Cancel

start_handler = CommandHandler('start', start_callback)
voice_is_received_handler = MessageHandler(
    filters.VOICE,
    voice_is_received_callback,
)
parse_voice_action_handler = CommandHandler("parse", parse_voice_callback)
save_note_handler = CommandHandler("save", save_note_callback)
cancel_handler = CommandHandler("cancel", cancel_callback)


name_conversation_handler = ConversationHandler(
        entry_points=[voice_is_received_handler],
        states={
            BotStates.VoiceReceivedActionRequested: [
                parse_voice_action_handler,
                cancel_handler,
            ],
            BotStates.VoiceIsParsed: [
                save_note_handler,
                cancel_handler,
            ],
        },
        fallbacks=[cancel_handler],
        conversation_timeout=settings.CONVERSATION_TIMEOUT,
    )
