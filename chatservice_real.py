import socket
import threading
import re

Packet_string= ""
neighbor_ip =[]
id_user=""
ip_sender=""
Packet_string_old=""

host = input("Enter Your IP Adress: ")
ip_string = input(f"Enter the address of neighbors (split with '&'): ")
first_mem=input("Are you a firt member? (yes|no) ")
neighbor_ip=ip_string.split('&')


def id_check(packet_id):

    global ip_sender
    
    ip_sender = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', packet_id)
    packet_id =packet_id.replace(ip_sender.group(),"")

    if "ID_USER" in packet_id:
            packet_id = packet_id.replace("ID_USER","")
            if packet_id == id_user:
                packet_id="choose ANOTHER id: "
                return packet_id
            else:
                return(f"\n{packet_id} joined.. ")



def th_server():
    global Packet_string
    global id_user
    global Packet_string_old
    Packet_string_new=""
    
    
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host,55555))
        server.listen()

        clientsocket,addr = server.accept()
        
        Packet_string_new= clientsocket.recv(1024).decode()
        if Packet_string_new != Packet_string_old :
            Packet_string=Packet_string_new
            if Packet_string =="choose ANOTHER id: ":
                id_user = input("choose ANOTHER id: ")
                Packet_string=f"\n{id_user} joined... "

            elif "ID_USER" in Packet_string:
                Packet_string=id_check(Packet_string)
            else:
                print(f"{Packet_string}")
            Packet_string_old=Packet_string_new

def th_client():
    global Packet_string
    global neighbor_ip
    global ip_sender
    
    while True:
         
      if Packet_string != ""  :  
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if Packet_string =="choose ANOTHER id: ": 
            c.connect((ip_sender.group(),55555))
            c.send((Packet_string).encode()) 

        
        else:
         for ip in neighbor_ip:
                c.connect((ip,55555))
                c.send((Packet_string).encode())
                #print(f'Sending {Packet_string} to : {ip}' )

            
        Packet_string= ""

client_thread = threading.Thread(target=th_client)
client_thread.start()

server_thread = threading.Thread(target=th_server)
server_thread.start()

id_user = input("choose an ID: ")

if first_mem=="no":
 Packet_string="ID_USER"+id_user+host
 

'''
while True:
    Packet_string_old = f'{id_user}: {input("")}'
    Packet_string=Packet_string_old
'''