import socket
import threading
import json
import time
import random

Packet_string = {
    "type": "",
    "ip": ""
}
neighbor_ip = []
id_user = ""
ip_sender = ""
prob_gossip = 0.5
final_neighbor_list = []
Packet_string_old = {
    "type": "",
    "ip": ""
}
packet_types = {
    "CHECK_USER_ID": "CHECK_USER_ID",
    "CHECK_USER_ID_RESPONSE": "CHECK_USER_ID_RESPONSE",
    "MESSAGE": "MESSAGE",
    "UPDATE_NEIGHBOR": "UPDATE_NEIGHBOR"
}
id_check_counter = 0

def id_check(packet):
    global packet_types
    global final_neighbor_list
    global id_check_counter
    global neighbor_ip

    packet_id = packet["id"]
    if packet_id == id_user:
        packet = {
            "type": packet_types["CHECK_USER_ID_RESPONSE"],
            "message": "refused",
            "ip": packet["ip"]
        }
        return packet

    elif packet_id != id_user:
        return ({
             "type": packet_types["CHECK_USER_ID"],
             "id": packet_id,
             "ip": packet["ip"]
           })

    else:
        return ({
            "type": packet_types["MESSAGE"],
            "message": f"\n{packet_id} joined.. ",
            "ip": Packet_string["ip"]
        })


def th_server():
    global Packet_string
    global id_user
    global Packet_string_old
    global packet_types
    global neighbor_ip
    Packet_string_new = {
        "type": "",
        "ip": ""
    }

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, 55555))
    server.listen()

    while True:
        clientsocket, addr = server.accept()
        Packet_string_new = json.loads(clientsocket.recv(1024).decode())
        if Packet_string_new["type"] == packet_types["UPDATE_NEIGHBOR"]:
            if Packet_string_new["ip"] not in neighbor_ip:
                neighbor_ip.append(Packet_string_new["ip"])
        elif Packet_string_new["type"] == packet_types["CHECK_USER_ID_RESPONSE"]:    
            Packet_string = Packet_string_new
            print(Packet_string_new["ip"] == host)
            if Packet_string_new["message"] == "refused" and Packet_string_new["ip"] == host:
                id_user = input("choose ANOTHER id: ")
                Packet_string = {
                    "type": packet_types["CHECK_USER_ID"],
                    "id": id_user,
                    "ip": Packet_string_new["ip"]
                }

            ''''
                Packet_string={
                    "type": packet_types["MESSAGE"],
                    "message" :f"\n{id_user} joined... ",
                    "ip": Packet_string["ip"]
                }
               '''
        elif Packet_string_new["type"] == packet_types["CHECK_USER_ID"]:
            Packet_string = id_check(Packet_string_new)

        else:
            if Packet_string_new != Packet_string_old:
                Packet_string = Packet_string_new
                print(Packet_string["message"])
            Packet_string_old = Packet_string_new


def th_client():
    global Packet_string
    global neighbor_ip
    global packet_types
    global final_neighbor_list
    global infected_nodes
    global first_mem

    if first_mem == "no":
        for ip in neighbor_ip:
            neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            neighbor_socket.connect((ip, 55555))
            neighbor_socket.send(json.dumps({
                "type": packet_types["UPDATE_NEIGHBOR"],
                "ip": host
            }).encode())

    while True:
        if len(infected_nodes) != len(neighbor_ip):
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if num_neighbor > 1:
                final_neighbor_list = random.sample(neighbor_ip, k=gossip)
            else:
                final_neighbor_list = neighbor_ip

            if Packet_string["type"] != "":
                if Packet_string["type"] == packet_types["CHECK_USER_ID_RESPONSE"] and Packet_string["ip"] in neighbor_ip:
                    c.connect((Packet_string["ip"], 55555))
                    c.send((json.dumps(Packet_string)).encode())
                    Packet_string = {
                        "type": "",
                        "ip": ""
                    }
                    infected_nodes.clear()

                else:
                    for ip in final_neighbor_list:
                        print("Packet_string", Packet_string)
                        if ip != Packet_string["ip"] and Packet_string["type"] != packet_types["CHECK_USER_ID_RESPONSE"]:
                            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            c.connect((ip, 55555))
                            c.send((json.dumps(Packet_string)).encode())
                            if ip not in infected_nodes:
                                infected_nodes.append(ip)
            infected_nodes.clear()
            Packet_string = {
                "type": "",
                "ip": ""
            }


host = input("Enter Your IP Address: ")


ip_string = input(f"Enter the address of neighbors (split with '&'): ")

first_mem = input("Are you a first member? (yes|no) ")
id_user = input("choose an ID: ")

neighbor_ip = ip_string.split('&')
infected_nodes = []


num_neighbor = len(neighbor_ip)
gossip = int((1-prob_gossip)*num_neighbor)

server_thread = threading.Thread(target=th_server)
server_thread.start()

client_thread = threading.Thread(target=th_client)
client_thread.start()


if first_mem == "no":
    Packet_string = {
        "type": packet_types["CHECK_USER_ID"],
        "id": id_user,
        "ip": host
    }

else:
    print(f"{id_user} joined...")


while True:
    time.sleep(1)
    if Packet_string["type"] == "":
        new_message = input("")
        Packet_string = {
            "type": packet_types["MESSAGE"],
            "ip": host,
            "message": id_user + ":" + new_message
        }
        # Packet_string=Packet_string_old
