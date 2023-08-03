import socket
import threading

HEADER = 64
PORT = 4321
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Quit"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT).lower()
            print(f"Concatenating {msg} to URL")
            print(f"Sending new URL to client")
            conn.send(str("en.m.wikipedia.org/wiki/" + msg).encode(FORMAT))
            connected = False
    conn.close()

def start():
    s.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
        print(f"[Active Connections] {threading.activeCount() - 1}")

print("[Starting] server is starting...")
start()