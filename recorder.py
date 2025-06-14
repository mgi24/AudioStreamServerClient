import soundcard as sc
import numpy as np
import scipy.io.wavfile

default_speaker = sc.default_speaker()
print(default_speaker)
default_mic = sc.default_microphone()
print(default_mic)

SAMPLE_RATE = 44100
CHANNELS = 2
CHUNK = 4096  # jumlah frame per buffer

mic = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)

with mic.recorder(samplerate=SAMPLE_RATE) as recorder:
    print("Streaming audio output... Tekan Ctrl+C untuk berhenti.")
    try:
        while True:
            data = recorder.record(numframes=CHUNK)
            pcm = (data * 32767).astype(np.int16)
            print(pcm.flatten())
    except KeyboardInterrupt:
        print("Stopped.")
