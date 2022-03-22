import socket 
import threading 
import os 
import sys
import tkinter as tk


class Send(threading.Thread): 
    def __init__(self, client, name): 
        super().__init__()
        self.name = name
        self.client = client
        self.DISCONNECT = "Q"
        self.FORMAT = "UTF-8"
        self.HEADER = 64

    def run(self): 

        while True: 
            print(f"{self.name}: ", end=" ")
            sys.stdout.flush()
            msg = sys.stdin.readline()[:-1]

            if msg == self.DISCONNECT: 
                self.client.sendall(f"CLIENT: {self.client.name} has left the chat".encode(self.FORMAT))
                break
            else: 
                self.client.sendall(f"{self.name}:a: {msg}".encode(self.FORMAT))

        print("\nQuitting...")
        self.client.close()
        os._exit(0)

class Recieve(threading.Thread): 
    def __init__(self, client, name): 
        super().__init__()
        self.name = name
        self.client = client
        self.messages = None
        self.FORMAT = "UTF-8"
        self.HEADER = 64

    def run(self): 

        while True: 
            msg = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg: 
                if self.messages: 
                    self.messages.insert(tk.END, msg)
                    print("hi")
                    print(f"\r{msg}\n{self.name}", end=" ")
                else: 
                    print(f"\r{msg}\n{self.name}: ", end=" ")
            else: 
                print(f"CLIENT: Connection was lost... ")
                self.client.close()
                os._exit(0)

class Client:
    def __init__(self, IP, PORT): 
        self.IP = IP
        self.PORT = PORT
        self.ADDR = (self. IP, self.PORT)
        self.FORMAT = "UTF-8"
        self.DISCONNECT = "Q"
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None 

    def start(self): 
        self.client.connect(self.ADDR) 
        print(f"CLIENT: Connected to {self.IP} {self.PORT}\n")

        self.name = input("Enter your username: ")
        print(f"Welcome, {self.name} Getting ready to send and recieve messages")

        send = Send(self.client, self.name)
        recieve = Recieve(self.client, self.name)

        send.start()
        recieve.start()

        self.client.sendall(f"SERVER: {self.name} has joined the chat!".encode(self.FORMAT))
        print("\rAll set! Leave the chatroom anytime by typing 'Q'\n")
        print(f"{self.name}: ", end=" ")

        return recieve

    def send(self, text_input): 
        msg = text_input.get()
        text_input.delete(0, tk.END)
        self.messages.insert(tk.END, f"{self.name}: {msg}")

        if msg == self.DISCONNECT: 
            self.client.sendall(f"SERVER: {self.name} has left the chat")
            print("\nQuitting....")
            self.client.close()
            os._exit()
        else: 
            self.client.sendall(f"{self.name} {msg}".encode(self.FORMAT))


def main(IP, PORT): 

    client = Client(IP, PORT)
    recieve = client.start()

    window = tk.Tk()
    window.title("Chatroom")

    frm_messages = tk.Frame(master=window)
    scrollbar = tk.Scrollbar(master=frm_messages)
    messages = tk.Listbox(master=frm_messages, yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    client.messages = messages
    recieve.messages = messages

    frm_messages.grid(row=0, column=0, columnspan=2, sticky="nsew")

    frm_entry = tk.Frame(master=window)
    text_input = tk.Entry(master=frm_entry)
    text_input.pack(fill=tk.BOTH, expand=True)
    text_input.bind("<Return>", lambda x: client.send(text_input))
    text_input.insert(0, "Enter your message: ")

    btn_send = tk.Button(master=window, text="Send", command=lambda: client.send(text_input))

    frm_entry.grid(row=1, column=0, padx=10, sticky="ew")
    btn_send.grid(row=1, column=1, pady=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=200, weight=0)

    window.mainloop()

if __name__ == "__main__": 
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5050
    main(IP, PORT)
