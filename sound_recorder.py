import sounddevice as sd
from scipy.io.wavfile import write
import uuid
import numpy as np


def record():
    fs = 44100
    seconds = 4

    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    print("Recording started...")
    sd.wait()  # Wait until recording is finished
    print("Recording finished...")
    path = f'recordings/{uuid.uuid4()}.wav'
    scaled = np.int16(recording / np.max(np.abs(recording)) * 32767)
    write(path, fs, scaled)  # Save as WAV file

    return path

