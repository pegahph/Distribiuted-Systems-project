import socket 
total_node= int(input("Enter number of members: "))
prob_gossip = int(input("With what probability do you want to communicate? (0.25|0.75|0.5)"))
host = input("Enter Session IP Adress: ")

mem_nei=int(total_node*prob_gossip)

ip_string = input(f"Enter the address of {mem_nei} neighbors (split with '&'): ")

Packet_string=""

while True:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, 55555))
    server.listen()

    print("Server is listening...")

    #while 1:
    clientsocket, address = server.accept()
    print(f'Connected with {str(address)}')

    Packet_string = clientsocket.recv(1024).decode()

    print(f"Node Received New Message: {Packet_string}")
    neighbor_ip =[]
    neighbor_ip=ip_string.split('&')

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for i in neighbor_ip:
        c.connect((i, 55555))
        c.send(Packet_string.encode())
        print(f'Sending Packet to : {i}' )

