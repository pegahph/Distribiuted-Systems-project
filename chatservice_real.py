import socket
import threading
import re
import json
import time

Packet_string= {
    "type": "",
    "ip": ""
}
neighbor_ip =[]
id_user=""
ip_sender=""
Packet_string_old={
    "type": "",
    "ip": ""
}
packet_types = {
    "CHECK_USER_ID": "CHECK_USER_ID",
    "CHECK_USER_ID_RESPONSE": "CHECK_USER_ID_RESPONSE",
    "MESSAGE": "MESSAGE"
}

host = input("Enter Your IP Address: ")
ip_string = input(f"Enter the address of neighbors (split with '&'): ")
first_mem=input("Are you a first member? (yes|no) ")
neighbor_ip=ip_string.split('&')


def id_check(packet):
    global packet_types
    global ip_sender
    
    # ip_sender = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', packet_id)
    ip_sender = packet["ip"]
    # packet_id =packet_id.replace(ip_sender.group(),"")
    packet_id = packet["id"]
    # packet_id = packet_id.replace("ID_USER","")
    if packet_id == id_user:
        packet={
            "type": packet_types["CHECK_USER_ID_RESPONSE"],
            "message": "choose ANOTHER id: ",
            "receiver_ip": packet["ip"]
        }
        return packet
    else:
        return({
            "type": packet_types["MESSAGE"],
            "message" :f"\n{packet_id} joined.. "
            })



def th_server():
    global Packet_string
    global id_user
    global Packet_string_old
    Packet_string_new={
        "type": "",
        "ip": ""
    }
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,55555))
    server.listen()

    while True:
        clientsocket,addr = server.accept()
        Packet_string_new= json.loads(clientsocket.recv(1024).decode())
        if Packet_string_new != Packet_string_old  :
            Packet_string=Packet_string_new
            if Packet_string["type"] == packet_types["CHECK_USER_ID_RESPONSE"]:
                id_user = input("choose ANOTHER id: ")
                Packet_string={
                    "type": packet_types["MESSAGE"],
                    "message" :f"\n{id_user} joined... ",
                    "ip": Packet_string_new["ip"]
                }

            elif Packet_string["type"] == packet_types["CHECK_USER_ID"] :
                Packet_string=id_check(Packet_string)
            else:
                print(Packet_string["message"])
            Packet_string_old=Packet_string_new

def th_client():
    global Packet_string
    global neighbor_ip
    global ip_sender
    
    while True:    
        if Packet_string["type"] != ""  :  
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if Packet_string["type"] == packet_types["CHECK_USER_ID_RESPONSE"]:
                c.connect((Packet_string["receiver_ip"],55555))
                c.send((json.dumps(Packet_string)).encode()) 

            
            else:
                for ip in neighbor_ip:
                    c.connect((ip,55555))
                    c.send((json.dumps(Packet_string)).encode())
                    #print(f'Sending {Packet_string} to : {ip}' )

                
            Packet_string= {
                "type": "",
                "ip": ""
            }

id_user = input("choose an ID: ")

if first_mem=="no":
#  Packet_string="ID_USER"+id_user+host
    Packet_string={
        "type": packet_types["CHECK_USER_ID"],
        "id": id_user,
        "ip": host
    }

client_thread = threading.Thread(target=th_client)
client_thread.start()

server_thread = threading.Thread(target=th_server)
server_thread.start()


while True:
    time.sleep(1)
    if Packet_string["type"] == "":
        new_message = input("")
        Packet_string_old = {
            "type": packet_types["MESSAGE"],
            "ip": host,
            "message": id_user + ":" + new_message
        }
        Packet_string=Packet_string_old
