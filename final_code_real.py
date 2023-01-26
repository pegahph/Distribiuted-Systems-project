
import socket 
import threading
import random
import json


Packet_string_old=""
Packet_string= ""
neighbor_ip =[]
final_neighbor_list=[]
prob_gossip=0.5


host = input("Enter Your IP Adress: ")
ip_string = input(f"Enter the address of neighbors (split with '&'): ")

neighbor_ip=ip_string.split('&')
num_neighbor = len(neighbor_ip)

if num_neighbor>1 :
    
    gossip= int((1-prob_gossip)*num_neighbor)
    final_neighbor_list= random.sample(neighbor_ip, k=gossip)
else:
    final_neighbor_list=neighbor_ip


def th_server():
    global Packet_string_old
    Packet_string_new=""
    global Packet_string
    
    
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host,55555))
        server.listen(5)

        clientsocket, address = server.accept()

        Packet_string_new = clientsocket.recv(1024).decode()

        if Packet_string_new != Packet_string_old :
            Packet_string=Packet_string_new
            print(f"Node Received New Message: {Packet_string}")
            Packet_string_old=Packet_string_new
        
    
def th_client():

    global final_neighbor_list
    global Packet_string
    
    while True:
      if Packet_string != ""  :  
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for ip in final_neighbor_list:
                c.connect((ip,55555))
                c.send(bytes(json.dumps(Packet_string).encode()))
                print(f'Sending Packet to : {ip}' )

            
        Packet_string= ""

client_thread = threading.Thread(target=th_client)
client_thread.start()

server_thread = threading.Thread(target=th_server)
server_thread.start()

while True:
    Packet_string_old = input() 
    Packet_string=Packet_string_old