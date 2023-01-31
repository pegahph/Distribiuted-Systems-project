
import socket 
import threading
import random
import json
from random import uniform
from time import sleep

PORT = 55555
Packet_string_old=""
Packet_string= {
    "clock": {},
    "packet": ""
}
neighbor_ip =[]
final_neighbor_list=[]
prob_gossip=0.5
neighbors_socket = {}
clock = 0
vector_clock = {}


def calculate_clock():
    global clock
    while True:
        clock += 1
        sleep(uniform(0.5, 1.5))

def th_server():
    global Packet_string_old
    Packet_string_new=""
    global Packet_string
    global clock
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,PORT))
    server.listen(5)
    while True:
        clientsocket, address = server.accept()
        receiver_ip, port = address
        Packet_string_new = json.loads(clientsocket.recv(1024).decode())
        if Packet_string_new["packet"] != Packet_string_old :
            for ip in Packet_string_new["clock"].keys():
                if ip not in vector_clock.keys():
                    vector_clock[ip] = 0
                vector_clock[ip] = max(Packet_string_new["clock"][ip], vector_clock[ip])
            if receiver_ip not in vector_clock.keys():
                vector_clock[receiver_ip] = 0
            vector_clock[receiver_ip] += 1
            Packet_string={"clock": vector_clock,"packet":Packet_string_new["packet"]}
            print(f"Node Received New Message: {Packet_string}")
            Packet_string_old=Packet_string_new
        
    
def th_client():

    global final_neighbor_list
    global Packet_string
    
    while True:
      if num_neighbor>1 :
            final_neighbor_list= random.sample(neighbor_ip, k=gossip)
      else:
            final_neighbor_list=neighbor_ip
            
      if Packet_string["packet"] != ""  :  
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for ip in final_neighbor_list:
            old_vector_clock = Packet_string["clock"]
            new_vector_clock = old_vector_clock
            new_vector_clock[host] +=1
            message_packet = {
                "clock": new_vector_clock,
                "packet": Packet_string["packet"]
            }
            c.connect((ip,PORT))
            c.send(bytes(json.dumps(message_packet).encode()))
            print(f'Sending Packet to : {ip}' )

            
        Packet_string= {"clock": vector_clock, "packet":""}

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
vector_clock[host] = 0
while True:
    Packet_string_old = input() 
    Packet_string={"clock": vector_clock, "packet":Packet_string_old}