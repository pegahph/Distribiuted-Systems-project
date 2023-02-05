
import socket
import threading
import random
import json

PORT = 55555   
Packet_string_old = ""
Packet_string = ""
neighbor_ip = []
final_neighbor_list = []
prob_gossip = 0.5
neighbors_socket = {}

def connect_neighbors():
    for ip in neighbor_ip:
        neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_socket.connect((ip,PORT))
        neighbors_socket[ip] = neighbor_socket


def th_server():
    global Packet_string_old
    Packet_string_new = ""
    global Packet_string

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, PORT))
    server.listen(5)

    while True:
        clientsocket, address = server.accept()
        Packet_string_new = json.loads(clientsocket.recv(1024).decode())

        if Packet_string_new != Packet_string_old:
            Packet_string = Packet_string_new
            print(f"Node Received New Message: {Packet_string}")
            Packet_string_old = Packet_string_new


def th_client():
    global final_neighbor_list
    global Packet_string

    while True:  
        gossip = int((1-prob_gossip)*num_neighbor)      
        if num_neighbor > 1:
            final_neighbor_list = random.sample(neighbor_ip, k=gossip)
        else:
            final_neighbor_list = neighbor_ip
            
        if Packet_string != "":          
            for ip in final_neighbor_list:
                neighbors_socket[ip].send(bytes(json.dumps(Packet_string).encode()))
                print(f'Sending Packet to : {ip}')
            Packet_string = ""



host = input("Enter Your IP Adress: ")
server_thread = threading.Thread(target=th_server)
server_thread.start()
ip_string = input(f"Enter the address of neighbors (split with '&'): ")
neighbor_ip = ip_string.split('&')
connect_neighbors()

num_neighbor = len(neighbor_ip)


client_thread = threading.Thread(target=th_client)
client_thread.start()


while True:
    Packet_string_old = input("Enter message: ")
    Packet_string = Packet_string_old
