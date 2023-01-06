import boto3

from tgbot.models import Note
from tgbot.settings import STORAGE_PATH


def save_note(note: Note):
    s3 = boto3.resource('s3')

    filename = f"{note.user_id}_{note.origin_voice_msg_id}.json"
    s3object = s3.Object(STORAGE_PATH, filename)

    s3object.put(
        Body=(bytes(note.json().encode('UTF-8'))),
    )

    return True
