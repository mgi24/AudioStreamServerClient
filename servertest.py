import socket
import threading
import wave
import time

SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345
CHUNK = 4096  # Jumlah byte per kirim (frame * channels * 2)

clients = set()
clients_lock = threading.Lock()

def handle_client(conn, addr, wav_params):
    print(f"Client {addr} connected.")
    with wave.open('comp1.wav', 'rb') as wf:
        while True:
            data = wf.readframes(CHUNK // (wav_params['sampwidth'] * wav_params['nchannels']))
            if not data:
                break
            try:
                conn.sendall(data)
            except (ConnectionResetError, BrokenPipeError, OSError):
                break
            # Streaming: delay sesuai durasi chunk
            time.sleep(CHUNK / (wav_params['framerate'] * wav_params['sampwidth'] * wav_params['nchannels']))
    conn.close()
    print(f"Client {addr} disconnected.")

def main():
    # Buka file WAV untuk mendapatkan parameter
    with wave.open('comp1.wav', 'rb') as wf:
        wav_params = {
            'nchannels': wf.getnchannels(),
            'sampwidth': wf.getsampwidth(),
            'framerate': wf.getframerate()
        }
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen()
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
    try:
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr, wav_params), daemon=True).start()
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()