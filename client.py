import soundcard as sc
import numpy as np
import socket

SERVER_IP = '127.0.0.1'   # Ganti dengan IP server
SERVER_PORT = 12345       # Ganti dengan port server
SAMPLE_RATE = 44100
CHANNELS = 2
CHUNK = 4096  # Harus sama dengan server

# Setup UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)
sock.sendto(b'hello', (SERVER_IP, SERVER_PORT))  # Daftarkan diri ke server

speaker = sc.default_speaker()

print(f"Listening audio stream dari {SERVER_IP}:{SERVER_PORT} ... Tekan Ctrl+C untuk berhenti.")
try:
    while True:
        data, _ = sock.recvfrom(CHUNK * CHANNELS * 2)  # 2 bytes per sample (int16)
        if len(data) < CHUNK * CHANNELS * 2:
            continue  # Skip jika data kurang
        pcm = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32767.0
        pcm = pcm.reshape(-1, CHANNELS)
        speaker.play(pcm, samplerate=SAMPLE_RATE)
except KeyboardInterrupt:
    print("Stopped.")
finally:
    sock.close()