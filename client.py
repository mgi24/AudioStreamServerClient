import soundcard as sc
import numpy as np
import socket

SERVER_IP = '127.0.0.1'   # Ganti dengan IP server
SERVER_PORT = 12345       # Ganti dengan port server
SAMPLE_RATE = 44100
CHANNELS = 2
CHUNK = 4096  # Harus sama dengan server

# Setup TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

speaker = sc.default_speaker()

print(f"Listening audio stream dari {SERVER_IP}:{SERVER_PORT} ... Tekan Ctrl+C untuk berhenti.")
try:
    while True:
        # Terima data sebanyak CHUNK * CHANNELS * 2 bytes (int16)
        data = b''
        expected_bytes = CHUNK * CHANNELS * 2
        while len(data) < expected_bytes:
            packet = sock.recv(expected_bytes - len(data))
            if not packet:
                break
            data += packet
        if len(data) < expected_bytes:
            continue  # Skip jika data kurang
        pcm = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32767.0
        pcm = pcm.reshape(-1, CHANNELS)
        speaker.play(pcm, samplerate=SAMPLE_RATE)
except KeyboardInterrupt:
    print("Stopped.")
finally:
    sock.close()