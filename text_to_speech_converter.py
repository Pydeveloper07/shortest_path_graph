import json
from google.cloud import texttospeech
import uuid

from credentials import get_credentials


def convert_text_to_speech(text):
    credentials = get_credentials()
    client = texttospeech.TextToSpeechClient.from_service_account_info(credentials)

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    file = f"responses/{uuid.uuid4()}.wav"
    with open(file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file \"{file.split("/")[-1]}\"')

    return file
