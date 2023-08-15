import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 1234
ADDR = (SERVER, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate
client_socket.bind(ADDR)

def url_creation(conn, addr):
    """Creates Gasbuddy url from requested region"""
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        data_received = conn.recv(256).decode('utf-8')  # receive response
        if data_received:
            data_received = int(data_received)
            region_url = conn.recv(data_received).decode('utf-8')
            print("Received from server: " + region_url)  # show in terminal to verify
            region_url = region_url.lower()
            region_url = f"https://www.gasbuddy.com/gasprices/oregon/{region_url}"
            conn.send(region_url.encode('utf-8'))  # send response
            print("Sent to server: " + region_url)
        connected = False
        conn.close()
def micro_program():
    client_socket.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = client_socket.accept()
        t = threading.Thread(target=url_creation, args=(conn, addr))
        t.start()
        print(f"[Active Connections] {threading.active_count() - 1}")
micro_program()