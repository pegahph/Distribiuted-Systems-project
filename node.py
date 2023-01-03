import socket
import threading


class Node:
    def __init__(self, neighbors):
        self.port = 5000
        self.host = socket.gethostbyname(socket.gethostname())
        self.neighbors = neighbors
        self.clientList = []
        if len(neighbors) == 0:
            self.runServer()
        else:
            self.nickname = input("Choose a nickname: ")
            self.runClient()

    def clientReceive(self):
        while True:
            try:
                for client in self.clientList:
                    message = client.recv(1024).decode("ascii")
                    if message == "NICK":
                        client.send(self.nickname.encode("ascii"))
                    else:
                        print(message)
            except:
                print("An error occurred!")
                client.close()
                break

    def clientWrite(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            for client in self.clientList:
                client.send(message.encode("ascii"))

    def runClient(self):
        for neighbor in self.neighbors:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientList.append(client)
            try:
                client = client.connect((neighbor, self.port))
                receive_thread = threading.Thread(
                    target=self.clientReceive)
                receive_thread.start()

                write_thread = threading.Thread(
                    target=self.clientWrite)
                write_thread.start()

            except:
                print(f'An error occurred! for ip {neighbor}')
                
        server_thread = threading.Thread(target=self.runServer)
        server_thread.start()

    def runServer(self):
        server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print("server is listening...")
        while True:
            client, address = server.accept()
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode("ascii"))
            nickname = client.recv(1024).decode("ascii")

            print(f'Nickname of the client is {nickname}')
            client.send("Connected to the server".encode("ascii"))


neighbors = []
haveOthersIpAddr = input(
    "Do you have your neighbors ip addresses? Enter yes/no \n")
if haveOthersIpAddr == "yes":
    print("Enter you Ip addresses separating with comma and no white spaces:")
    neighbors = input().split(',')

node = Node(neighbors)
