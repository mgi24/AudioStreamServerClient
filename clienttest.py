import socket
import numpy as np
import soundcard as sc

SERVER_IP = '127.0.0.1'   # Ganti dengan IP server jika perlu
SERVER_PORT = 12345
CHUNK = 4096              # Harus sama dengan server
CHANNELS = 2              # Stereo
SAMPLE_RATE = 44100       # 44.1kHz

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

speaker = sc.default_speaker()
print(f"Speaker: {speaker.name} ({speaker.channels})")

print(f"Menerima audio stream dari {SERVER_IP}:{SERVER_PORT} ... Tekan Ctrl+C untuk berhenti.")
try:
    while True:
        data = b''
        expected_bytes = CHUNK
        while len(data) < expected_bytes:
            packet = sock.recv(expected_bytes - len(data))
            if not packet:
                break
            data += packet
        if len(data) < expected_bytes:
            break  # Selesai
        # Ubah data ke float32 untuk soundcard
        pcm = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32767.0
        pcm = pcm.reshape(-1, CHANNELS)
        print(pcm)
except KeyboardInterrupt:
    print("Stopped.")
finally:
    sock.close()