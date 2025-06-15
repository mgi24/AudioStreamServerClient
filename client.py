import socket

CLIENT_IP = '0.0.0.0'   # Listen di semua interface
CLIENT_PORT = 5005      # Port UDP yang sama dengan server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_IP, CLIENT_PORT))

print(f"Listening UDP audio di {CLIENT_IP}:{CLIENT_PORT} ... Tekan Ctrl+C untuk berhenti.")
try:
    while True:
        data, addr = sock.recvfrom(4096)  # Ukuran buffer bisa disesuaikan
        print(data)  # Print raw byte data
except KeyboardInterrupt:
    print("Stopped.")
finally:
    sock.close()