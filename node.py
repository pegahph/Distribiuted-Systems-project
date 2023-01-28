import socket
import threading
import json
import random

probability = 0.5
class Node:
    def __init__(self, port:int, host:str, neighbors:set):
        self.port = port
        self.host = host
        self.neighbors = neighbors
        self.accessibleNodes = []
        self.clients = []
        self.nickname = input("Choose a nickname: ")
        if len(neighbors) == 0:
            self.runServer()
        else:
            self.runClient()

    def clientReceive(self):
        while True:
            try:
                for client in self.clients:
                    message = json.loads(client.recv(1024).decode("ascii"))
                    print(f'Received a message: {message}')
            except:
                print("An error occurred!")
                client.close()
                break

    def clientWrite(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            gossip= int((1- probability)*len(self.neighbors))
            self.accessibleNodes= random.sample(self.clients, k=gossip)
            for client in self.accessibleNodes:
                host, port = client.getpeername()
                client.send(bytes(json.dumps(message).encode()))
                print(f'Sending Packet to : {host}' )

    def runClient(self):
        for neighbor in self.neighbors:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clients.append(client)
            try:
                client = client.connect((neighbor, self.port))
                receive_thread = threading.Thread(
                    target=self.clientReceive)
                receive_thread.start()

                write_thread = threading.Thread(
                    target=self.clientWrite)
                write_thread.start()

            except Exception as e:
                print(e)
                print(f'An error occurred! for ip {neighbor}')

        server_thread = threading.Thread(target=self.runServer)
        server_thread.start()

    def runServer(self):
        print("ip", self.host)
        server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(f"{self.nickname}'s server is listening...")
        while True:
            client, address = server.accept()
            print(f'Connected with {str(address)}')
            # client.send("Connected to the server".encode("ascii"))


neighbors = []
port = 5000
host = socket.gethostbyname(socket.gethostname())

haveOthersIpAddr = input(
    "Do you have your neighbors ip addresses? Enter yes/no \n")
if haveOthersIpAddr == "yes":
    print("Enter you Ip addresses separating with comma and no white spaces:")
    neighbors = input().split(',')
    host = input("Enter your Ip: \n")

node = Node(port, host, neighbors)
