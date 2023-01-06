import asyncio
import json
import logging

from telegram import Update

import tgbot.settings as settings
from tgbot.bot import build_application

# Logger setup
logging.getLogger().setLevel('INFO')
logging.info('Starting bot')


application = build_application()


def lambda_handler(event, context):
    result = asyncio.get_event_loop().run_until_complete(main(event, context))

    return {
        'statusCode': 200,
        'body': result
    }


async def main(event, context):
    if not settings.LOCAL_MODE:
        return await handle_update(event)


async def handle_update(event):
    try:
        logging.info('Processing update...')
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(event["body"]), application.bot)
        )
        logging.info(f'Processed update {event["body"]}')
        return 'Success'

    except Exception as exc:
        logging.info(f"Failed to process update with {exc}")
    return 'Failure'


def debug_main():
    application.run_polling()


if __name__ == '__main__':
    if settings.LOCAL_MODE:
        debug_main()
