import socket
import soundcard as sc
import numpy as np

# Konfigurasi
SERVER_IP = '0.0.0.0'      # Listen di semua interface
SERVER_PORT = 5005         # Port UDP tujuan
CLIENT_IP = '192.168.0.104'  # Ganti dengan IP client ESP32 atau PC
CLIENT_PORT = 5005         # Port UDP client
SAMPLE_RATE = 44100
CHUNK = 1024               # Jumlah frame per buffer

# Siapkan socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Siapkan soundcard loopback
mic = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)

with mic.recorder(samplerate=SAMPLE_RATE) as recorder:
    print(f"Streaming audio output ke {CLIENT_IP}:{CLIENT_PORT} via UDP ... Tekan Ctrl+C untuk berhenti.")
    try:
        while True:
            data = recorder.record(numframes=CHUNK)  # shape: (CHUNK, 2)
            mono_data = np.mean(data, axis=1)        # convert to mono
            pcm = (mono_data * 32767).astype(np.int16)
            sock.sendto(pcm.tobytes(), (CLIENT_IP, CLIENT_PORT))
    except KeyboardInterrupt:
        print("Streaming stopped by user.")
    finally:
        sock.close()