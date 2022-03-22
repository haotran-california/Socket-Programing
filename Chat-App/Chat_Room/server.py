import socket 
import threading 
import os 
import datetime

class Server(threading.Thread): 

    def __init__(self, IP, PORT):
        super().__init__()
        #socket settings
        self.IP = IP
        self.PORT = PORT
        self.ADDR = (IP, PORT)

        #server data
        self.activeConnections = 0
        self.connectionList = []
        self.users = {}

    def run(self): 
        #Server setup
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.ADDR)
        server.listen(1)

        print(f"SERVER: Started on {self.IP} {self.PORT}")
        while(True): 
            #Accept Connection 
            connection, address = server.accept()
            print(f"SERVER: Accepted a connection from {connection.getpeername()}")
            

            #Open a thread for each new connection 
            client = ClientSocket(connection, self, address)
            client.start()

            #Add meta data
            self.connectionList.append(client)
            self.activeConnections = len(self.connectionList) 
            print(f"Read to recieve messages from {client.client.getpeername()}")
            print(f"SERVER: The number of users are {self.activeConnections}")
            

    def broadcast(self, msg, source):
        #UNICAST: one-to-one transmissions to each individual connected client 
        for connection in self.connectionList: 
            if connection.name != source: 
                connection.send(f"{msg}")

    def addUsername(self, client): 

        pass 
            

class ClientSocket(threading.Thread): 
    def __init__(self, client, server, name): 
        super().__init__()
        self.client = client
        self.name = name
        self.server = server
        self.FORMAT = "UTF-8"
        self.HEADER = 64

    def run(self): 
        while True: 
            msg = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg: 
                self.server.broadcast(msg, self.name)
                print(f"SERVER: Broadcasted {msg} to Number of Users: {self.server.activeConnections}")
            else: 
                server.connectionList.remove(self.client)
                self.client.close()
                print(f"SERVER: Connection with {self.client.name} has been closed")
                return 
                
    def send(self, msg):
        self.client.sendall(msg.encode(self.FORMAT))

def exit(server): 
    while True: 
        ipt = input("")
        if ipt.upper() == "Q": 
            print("SERVER: closing all connections...")
            for connection in server.connectionList: 
                connection.client.close()
            print("SERVER: Shutting down server...")
            os._exit(0)
        


if __name__ == "__main__": 
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5050

    server = Server(IP, PORT)
    server.start()

    exit = threading.Thread(target = exit, args = (server, ))
    exit.start()

