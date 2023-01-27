import socket
import threading
import json

class Node:
    def __init__(self, port, host, neighbors, probability):
        self.port = port
        self.host = host
        self.neighbors = neighbors
        self.clients = []
        self.probability = probability
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
                    if message['PROB']:
                        self.probability = message["PROB"]
                        print(self.probability)

            except:
                print("An error occurred!")
                client.close()
                break

    def clientWrite(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            for client in self.clients:
                client.send(message.encode("ascii"))

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
            self.clients.append(client)
            print(client)
            data = {"PROB": self.probability}
            client.send(json.dumps(data).encode("ascii"))
            # client.send("Connected to the server".encode("ascii"))


neighbors = []
probability = None
port = 5000
host = socket.gethostbyname(socket.gethostname())

haveOthersIpAddr = input(
    "Do you have your neighbors ip addresses? Enter yes/no \n")
if haveOthersIpAddr == "yes":
    print("Enter you Ip addresses separating with comma and no white spaces:")
    neighbors = input().split(',')
    host = input("Enter your Ip: \n")
else:
    probability = float(input("Enter the probability: \n"))

node = Node(port, host, neighbors, probability)
