import socket

HEADER = 256
PORT = 4321
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Quit"
SERVER = "10.197.134.205"
ADDR = (SERVER, PORT)

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(ADDR)

def send():
    valid_input = True
    while valid_input == True:
        msg = input("Please enter a theme park: ")
        if msg.lower() in ["disneyland", "sixflags"]:
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            c.send(send_length)
            c.send(message)
            data = c.recv(2048).decode(FORMAT)
            print("Data has been sent to microservice\n")
            print("Data received from microservice:")
            print(data)
            valid_input = False
        else:
            print(f"That is not a valid theme park name. Try again.")
send()