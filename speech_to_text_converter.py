import json
from google.cloud import speech
import io

from credentials import get_credentials


def convert_speech_to_text(audio_path):
    credentials = get_credentials()
    speech_client = speech.SpeechClient.from_service_account_info(credentials)

    with io.open(audio_path, "rb") as file:
        content = file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )

    response = speech_client.recognize(config=config, audio=audio)

    result = response.results[0].alternatives[0].transcript
    print("Transcript: {}".format(result))

    return result



