
import socket 
import threading
import random
import json
from random import uniform
from time import sleep

PORT = 55555
Packet_string_old=""
Packet_string= ""
neighbor_ip =[]
final_neighbor_list=[]
prob_gossip=0.5
neighbors_socket = {}
clock = 0


def calculate_clock():
    global clock
    while True:
        clock += 1
        sleep(uniform(0.5, 1.5))

def th_server():
    global Packet_string_old
    Packet_string_new=""
    global Packet_string

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,PORT))
    server.listen(5)
    while True:
        clientsocket, address = server.accept()

        Packet_string_new = json.loads(clientsocket.recv(1024).decode())
        clock = max(Packet_string_new["clock"], clock) + 1

        if Packet_string_new["packet"] != Packet_string_old :
            Packet_string=Packet_string_new["packet"]
            print(f"Node Received New Message: {Packet_string}")
            Packet_string_old=Packet_string_new
        
    
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
                message_packet = {
                    "clock": clock + 1,
                    "packet": Packet_string
                }
                neighbors_socket[ip].send(bytes(json.dumps(message_packet).encode()))
                print(f'Sending Packet to : {ip}')

            
        Packet_string= ""

clock_thread = threading.Thread(target=calculate_clock)
clock_thread.start()
host = input("Enter Your IP Adress: ")
ip_string = input(f"Enter the address of neighbors (split with '&'): ")

neighbor_ip=ip_string.split('&')
num_neighbor = len(neighbor_ip)
gossip= int((1-prob_gossip)*num_neighbor)

server_thread = threading.Thread(target=th_server)
server_thread.start()

client_thread = threading.Thread(target=th_client)
client_thread.start()

while True:
    Packet_string_old = input() 
    Packet_string=Packet_string_old