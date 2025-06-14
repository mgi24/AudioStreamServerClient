import soundcard as sc
import numpy as np
import threading
import socket
from queue import Queue

default_speaker = sc.default_speaker()
print(default_speaker)
default_mic = sc.default_microphone()
print(default_mic)

SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER_IP, SERVER_PORT))
sock.listen()

SAMPLE_RATE = 44100
CHUNK = 1024  # jumlah frame per buffer

clients = set()
clients_lock = threading.Lock()
client_queues = {}

def handle_client(conn, addr):
    print(f"Client {addr} connected.")
    with clients_lock:
        clients.add(conn)
    try:
        while True:
            # Hanya untuk menjaga koneksi tetap hidup, tidak menerima data dari client
            data = conn.recv(1)
            if not data:
                break
    except Exception as e:
        print(f"Client {addr} error: {e}")
    finally:
        with clients_lock:
            clients.discard(conn)
        conn.close()
        print(f"Client {addr} disconnected.")

def accept_clients():
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def client_sender(conn, data_queue):
    while True:
        data = data_queue.get()
        if data is None:
            break
        try:
            conn.sendall(data)
        except (ConnectionResetError, BrokenPipeError, OSError):
            break

mic = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)

threading.Thread(target=accept_clients, daemon=True).start()

with mic.recorder(samplerate=SAMPLE_RATE) as recorder:
    print(f"Streaming audio output ke semua client TCP yang connect ke {SERVER_IP}:{SERVER_PORT} ... Tekan Ctrl+C untuk berhenti.")
    try:
        while True:
            data = recorder.record(numframes=CHUNK)  # shape: (CHUNK, 2)
            mono_data = np.mean(data, axis=1)  # convert to mono
            pcm = (mono_data * 32767).astype(np.int16)
            with clients_lock:
                for conn in list(clients):
                    if conn not in client_queues:
                        q = Queue()
                        client_queues[conn] = q
                        threading.Thread(target=client_sender, args=(conn, q), daemon=True).start()
                    try:
                        client_queues[conn].put_nowait(pcm.tobytes())
                    except Exception:
                        clients.discard(conn)
                        client_queues.pop(conn, None)
    except KeyboardInterrupt:
        print("Stopped.")
        sock.close()
