import socket 

host='192.168.10.2'
nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.10.1', 55555))




def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def swich_to_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, 55555))
    server.listen()


receive()
swich_to_server()









