import socket 


host = '192.168.10.1' #localhost


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, 55555))
server.listen()


def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
       ## nicknames.append(nickname)
       ## clients.append(client)

        print(f'Nickname of the client is {nickname}')
        ##broadcast(f'{nickname} joined the chat!'.encode("ascii"))
        client.send(f'Connected to the {host}'.encode("ascii"))





print("Server is listening...")
receive()