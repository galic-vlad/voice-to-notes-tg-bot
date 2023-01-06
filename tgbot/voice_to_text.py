from deepgram import Deepgram

from tgbot.models import DeepgramResponse


def get_summary_from_text(text: str) -> str:
    # TODO(@galic-vlad): separate `summary` and `title` fields of a note.
    return f"{text[:60]}..."


async def get_note(response: dict) -> DeepgramResponse:
    text = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    summaries = response["results"]["channels"][0]["alternatives"][0]["summaries"]
    if summaries:
        summary = summaries[0]["summary"]
    else:
        summary = get_summary_from_text(text)

    return DeepgramResponse(text, summary)


async def parse_voice_message(
        dg_client: Deepgram,
        voice_msg_url: str,
) -> DeepgramResponse:
    source = {'url': voice_msg_url}
    options = {
        "punctuate": True,
        "model": "general",
        "language": "en-US",
        "tier": "enhanced",
        "summarize": True,
    }

    response = await dg_client.transcription.prerecorded(source, options)
    text = await get_note(response)

    return text
