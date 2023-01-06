"""
Bot for voice-to-text messages.
"""

import logging

from telegram.ext import AIORateLimiter, ApplicationBuilder

import tgbot.settings as settings
from tgbot.handlers import name_conversation_handler, start_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def build_application():
    application = ApplicationBuilder() \
        .token(settings.TG_TOKEN) \
        .rate_limiter(AIORateLimiter(overall_max_rate=settings.RATE_LIMIT)) \
        .build()

    application.add_handler(start_handler)
    application.add_handler(name_conversation_handler)

    return application


def main():
    application = ApplicationBuilder().token(settings.TG_TOKEN).build()

    application.add_handler(start_handler)
    application.add_handler(name_conversation_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
