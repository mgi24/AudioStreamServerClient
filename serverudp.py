import socket
import soundcard as sc
import numpy as np

# Konfigurasi
BROADCASTIP = '192.168.0.255'      # Broadcast ip (ending 255) sending to all ip
CLIENT_PORT = 5005         # Port UDP client
SAMPLE_RATE = 44100
CHUNK = 720              # Jumlah frame per buffer

# Siapkan socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Siapkan soundcard loopback
mic = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)

with mic.recorder(samplerate=SAMPLE_RATE) as recorder:
    print(f"Streaming audio output ke {CLIENT_PORT} via UDP ... Tekan Ctrl+C untuk berhenti.")
    try:
        while True:
            data = recorder.record(numframes=CHUNK)  # shape: (CHUNK, 2)
            mono_data = np.mean(data, axis=1)        # convert to mono
            pcm = (mono_data * 32767).astype(np.int16)
            sock.sendto(pcm.tobytes(), (BROADCASTIP, CLIENT_PORT))
    except KeyboardInterrupt:
        print("Streaming stopped by user.")
    finally:
        sock.close()