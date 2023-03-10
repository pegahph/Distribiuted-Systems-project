import socket
import threading
import json
import time
import random

PORT = 55555
prob_gossip = 0.5
clients = {}
packet_types = {
    "JOIN_REQUEST": "JOIN_REQ",
    "CHECK_USER_ID_RESPONSE": "CHECK_USER_ID_RESPONSE",
    "MESSAGE": "MSG",
    "UPDATE_NEIGHBOR": "UPDATE_NEIGHBOR",
    "REPLY_MESSAGE": "REPLY_MESSAGE",
}
packet = {
    "type": ""
}
history = {}

print("Welcome to this chat service, to enter the reply mode, enter @'replied message'")
is_first_mem = input("Are you a first member? (y|n) ")
host = input('Enter your ip address: ')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, PORT))
server.listen()
neighbors = []
if is_first_mem == "n":
    neighbors = input(
        "Enter the address of neighbors (split with '&'): ").split('&')
id = input("choose an ID: ")


def initialClients():
    for ip in neighbors:
        clients[ip] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clients[ip].connect((ip, PORT))
        clients[ip].send((json.dumps(
            {"type": packet_types["UPDATE_NEIGHBOR"], "sender_ip": host})).encode())


def receiveMessage():
    global packet
    global clients
    global neighbors
    global history
    while True:
        client_socket, addr = server.accept()
        new_packet = json.loads(client_socket.recv(1024).decode())
        if new_packet["type"] == packet_types["UPDATE_NEIGHBOR"]:
            if new_packet["sender_ip"] not in clients.keys():
                neighbors.append(new_packet["sender_ip"])
                clients[new_packet["sender_ip"]] = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
        elif new_packet["type"] == packet_types["JOIN_REQUEST"]:
            new_packet["ip"].append(host)
            packet = new_packet
            print(f'{new_packet["id"]} joined the chat!')
        elif new_packet["type"] == packet_types["REPLY_MESSAGE"]:
            if new_packet["id"] in history.keys():
                history[new_packet["id"]].append(new_packet["message"])
            else:
                history[new_packet["id"]] = [new_packet["message"]]
            new_packet["ip"].append(host)
            packet = new_packet
            print(f'{new_packet["id"]}: {new_packet["message"]}')
            print(f'\tReply to {new_packet["reply_to"]}')
        elif new_packet["type"] == packet_types["MESSAGE"]:
            new_packet["ip"].append(host)
            packet = new_packet
            if new_packet["id"] in history.keys():
                history[new_packet["id"]].append(new_packet["message"])
            else:
                history[new_packet["id"]] = [new_packet["message"]]
            print(f'{new_packet["id"]}: {new_packet["message"]}')

def sendMessage():
    global packet
    global neighbors
    while True:
        susceptible_nodes = neighbors.copy()
        if packet["type"] != "":
            while len(susceptible_nodes) > 0:
                if len(neighbors) > 1:
                    gossip = int((1-prob_gossip)*len(neighbors))
                    infected_nodes = random.sample(susceptible_nodes, k=gossip)
                else:
                    infected_nodes = susceptible_nodes
                for ip in infected_nodes:
                    susceptible_nodes.remove(ip)
                    if ip not in packet["ip"]:                    
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((ip, PORT))
                        client.send((json.dumps(packet)).encode())
            packet = {
                "type": ""
            }


server_thread = threading.Thread(target=sendMessage)
server_thread.start()

client_thread = threading.Thread(target=receiveMessage)
client_thread.start()

if is_first_mem == "n":
    initialClients()
    packet = {
        "type": packet_types["JOIN_REQUEST"],
        "id": id,
        "ip": [host],
    }
    print(f'\nyou joined the chat!')
else:
    print(f'\nyou started a chat!')

while True:
    time.sleep(1)
    new_message = input("")
    if "@" in new_message:
        reply_to = new_message[1: ]
        split_message = reply_to.split(":")
        replied_id = split_message[0]
        replied_message = split_message[1][1: ]
        if replied_id not in history.keys():
            print("the user you entered does not exist, make sure you entered the correct form.")
        elif replied_message not in history[replied_id]:
            print("sorry, this message does not exist! make sure you entered the correct form.")
        else:
            message = input("\t")
            packet = {
                "type": packet_types["REPLY_MESSAGE"],
                "reply_to": reply_to,
                "message": message,
                "id": id,
                "ip": [host]
            }
    else:
        packet = {
            "type": packet_types["MESSAGE"],
            "message": new_message,
            "id": id,
            "ip": [host]
        }
