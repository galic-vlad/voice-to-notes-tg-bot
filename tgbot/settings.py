import os

import dotenv

LOCAL_MODE = False
if LOCAL_MODE:
    dotenv.load_dotenv("../local.env")

# Telegram
TG_TOKEN = os.getenv("TG_API_TOKEN")

# deepgram
DEEPGRAM_API_TOKEN = os.getenv("DEEPGRAM_API_TOKEN")

# Bot's settings
CONVERSATION_TIMEOUT = 60*3  # 3 minutes
RATE_LIMIT = 5

# Storage
STORAGE = "local_fs"
STORAGE_PATH = os.getenv("S3_STORAGE_PATH")
