import soundcard as sc
import numpy as np
import threading
import socket

default_speaker = sc.default_speaker()
print(default_speaker)
default_mic = sc.default_microphone()
print(default_mic)

SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

SAMPLE_RATE = 44100
CHUNK = 4096  # jumlah frame per buffer

clients = set()

def listen_clients():
    while True:
        data, addr = sock.recvfrom(16)
        clients.add(addr)



mic = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)

threading.Thread(target=listen_clients, daemon=True).start()

with mic.recorder(samplerate=SAMPLE_RATE) as recorder:
    print(f"Streaming audio output (mono) ke semua client UDP yang connect ke {SERVER_IP}:{SERVER_PORT} ... Tekan Ctrl+C untuk berhenti.")
    try:
        while True:
            data = recorder.record(numframes=CHUNK)  # shape: (CHUNK, 2)
            pcm = (data * 32767).astype(np.int16)
            for addr in list(clients):
                try:
                    sock.sendto(pcm.tobytes(), addr)
                except Exception:
                    clients.discard(addr)
    except KeyboardInterrupt:
        print("Stopped.")
        sock.close()
