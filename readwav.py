import wave
import numpy as np
import soundcard as sc
import time
import threading
import queue

FILENAME = 'comp1.wav'
CHUNK = 4096  # Jumlah byte per baca

with wave.open(FILENAME, 'rb') as wf:
    channels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    framerate = wf.getframerate()

    print(f"Channels: {channels}, Sample Width: {sampwidth}, Frame Rate: {framerate}")
    speaker = sc.default_speaker()
    print(f"Speaker: {speaker.name} ({speaker.channels})")
    print(f"Playing {FILENAME} in real-time...")
    pcm_queue = queue.Queue(maxsize=5)
    stop_flag = threading.Event()

    def reader_thread():
        while not stop_flag.is_set():
            data = wf.readframes(CHUNK)
            if not data:
                break
            pcm = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32767.0
            pcm_queue.put(pcm)
        stop_flag.set()

    t = threading.Thread(target=reader_thread)
    t.start()

    while not stop_flag.is_set() or not pcm_queue.empty():
        try:
            pcm = pcm_queue.get()
            speaker.play(pcm, samplerate=framerate*2, channels=channels)
        except queue.Empty:
            continue

    t.join()
        