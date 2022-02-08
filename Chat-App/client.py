from socket import * 
from threading import *

#CONSTANTS
IP = gethostbyname(gethostname())
PORT = 5050
ADDR = (IP, PORT)
HEADER = 4
FORMAT = "utf-8"
DISCONNECT = "Q"

#CLIENT SETUP
client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)
print(f"CLIENT: Connected to {IP} {PORT}")

#DATA
username = False

#DEFINE CHAT HANDLING FUNCTIONS
def sendMessage(): 
    userInput = input()
    if userInput: 
        #send header
        msgLength = str(len(userInput))
        padding = " " * (HEADER - len(msgLength))
        header = msgLength + padding
        client.send(header.encode(FORMAT)) 
        #send message 
        client.send(userInput.encode(FORMAT))

def listenMessages():
    while connected: 
        msgLength = int(client.recv(HEADER))
        msgContent = client.recv(msgLength).decode(FORMAT)
        print(f"{msgContent}")

#CLIENT EVENT LOOP
print("Running...")
connected = True
while connected: 
    if username: 
        print("Enter Message: ", end="")
    else: 
        print("Enter Username: ", end="")
        username = True 
    sendMessage()
    thread = Thread(target=listenMessages, args=())
    thread.start()
    
