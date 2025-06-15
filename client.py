import socket
import soundcard as sc
import numpy as np

default_speaker = sc.default_speaker()
print(f"Default speaker: {default_speaker.name}")
CLIENT_IP = '0.0.0.0'   # Listen di semua interface
CLIENT_PORT = 5005      # Port UDP yang sama dengan server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_IP, CLIENT_PORT))

print(f"Listening UDP audio di {CLIENT_IP}:{CLIENT_PORT} ... Tekan Ctrl+C untuk berhenti.")
try:
    while True:
        data, addr = sock.recvfrom(4096)  # Ukuran buffer bisa disesuaikan
        # Parse buffer ke PCM 44.1kHz, 16bit, mono
        pcm = np.frombuffer(data, dtype=np.int16)
        print(f"Received {len(pcm)} samples")
        # Jika ingin memutar, gunakan default_speaker.play(pcm.astype(np.float32) / 32768, samplerate=44100)
except KeyboardInterrupt:
    print("Stopped.")
finally:
    sock.close()