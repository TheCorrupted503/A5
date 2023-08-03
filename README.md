# Communication Contract

To request data from the microsservice, you must create a function that connects to the microserver using 
the python socket function socket.socket(socket.AF_INET, socket.SOCK_STREAM), and use the .bind() function
to connect to the microservice with the same HOST and PORT data and the .send() socket function to send a 
valid theme park name that has been encoded using 'utf-8' as the format.

example funciton:

PORT = 54321
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

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
c.send(message) <-------- # this function will send the user input to the microservice and request data.
data = c.recv(2048).decode(FORMAT) <-------- # this function will receive microservice data as a string.
print("Data has been sent to microservice\n")
print("Data received from microservice:")
print(data)
valid_input = False
else:
print(f"That is not a valid theme park name. Try again.")
send()

Example call:
Please enter a theme park: a
That is not a valid theme park name. Try again.
Please enter a theme park: disneyland
Data has been sent to microservice

Data received from microservice
en.m.wikipedia.org/wiki/disneyland


To recieve data from the microservice you must use the python socket function .recv() and decode it using 'utf-8'
as the format in order to use it throughout your program as a string.


![Sequence Diagram](/images/A9-1.png?raw=true "UML Sequence Diagram")