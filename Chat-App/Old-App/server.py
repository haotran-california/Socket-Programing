from socket import * 
from select import * 

#CONSTANTS
IP = gethostbyname(gethostname())
PORT = 5050
ADDR = (IP, PORT)
HEADER = 4
FORMAT = "utf-8"
DISCONNECT = "Q"

#SERVER SETUP
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"SERVER: Started on {IP} {PORT}")

#DATA
socketList = []
userHash = {}
numUsers = 0
socketList.append(server)

#DEFINE FUNCTIONS HANDLING MESSAGES 
def addUser(connection, address):
    msgLength = int(connection.recv(HEADER))
    username = connection.recv(msgLength).decode(FORMAT)
    userHash[address] = username
    print(f"SERVER: The address {address} has been added with the username {username}")

def getMessage(connection): 
    address = connection.getpeername()
    name = userHash[address]
    msgLength = int(connection.recv(HEADER))
    msgContent = connection.recv(msgLength).decode(FORMAT)
    print(f"SERVER: SENDER: {name} CONTENT: {msgContent}")
    return msgContent

def broadcastMessage(connection, msg): 
    address = connection.getpeername()
    name = userHash[address]
    for socket in socketList: 
        if socket != connection and socket != server: 
            newMessage = f"USER: {name} {msg}" 
            msgLength = str(len(newMessage))
            socket.send(msgLength.encode(FORMAT))
            socket.send(newMessage.encode(FORMAT))
            print(f"SERVER: Broadcasted {msg} to Number of Users: {numUsers - 1}")

def sendDisconnect(connection): 
    address = connection.getpeeername()
    name = userHash[address]
    msg = f"{name} been disconnected from the server"
    msgLength = str(len(msg))
    connection.send(msgLength)
    connection.send(msg.encode(FORMAT))

#SERVER EVENT LOOP
print("SERVER: Running...")
connected = True 
while connected:
    readSockets, _, _ = select(socketList, [], [])
    for notifedSocket in readSockets: 
        if notifedSocket == server: 
            connection, address = server.accept()
            socketList.append(connection)
            addUser(connection, address)
            numUsers = len(socketList) - 1
            print(f"SERVER: The number of users are {numUsers}")
        else: 
            msg = getMessage(notifedSocket)
            if(msg == DISCONNECT): 
                address = notifedSocket.getpeername()
                name = userHash[address]
                numUsers -= 1 
                notifedSocket.close()
                sendDisconnect()
                print(f"SERVER: {name} has disconnected ACTIVE CONNECTIONS: {numUsers}")
            else: 
                broadcastMessage(notifedSocket, msg)
            
        



