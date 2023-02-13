import socket 
import threading
import random
import time
import json
from random import uniform
from time import sleep

clock = 0
Packet_string= {
    "clock": clock,
    "packet": ""
}
recieved_ports_list=[]

round=[]

thread_count=1000
max_nei=(thread_count*10)
NeiCout=[]
sum_nei=0
difvalue=0
counter=0
port_start=20000


for i in range(0,thread_count):
      NeiCout.append(random.randint(1, thread_count-1))
      sum_nei+=NeiCout[i]

if max_nei > sum_nei:
      difvalue=1
else:
      difvalue=-1

while max_nei != sum_nei :
      if NeiCout[counter]<thread_count-1 and NeiCout[counter]+difvalue>=1:
            NeiCout[counter]+=difvalue
            sum_nei+=difvalue
            
      if counter < thread_count-1:
            counter+=1
      else:
            counter=0


           
def calculate_clock():
    global clock
    while True:
        clock += 1
        sleep(uniform(0.5, 1.5))


def mesg(th_no, port, port_count):
    print(f"thread no.{th_no} on port {port} Starting...  ")
    global recieved_ports_list
    global clock
    global round
    Neighbours_port=[]


    clock_thread = threading.Thread(target=calculate_clock)
    clock_thread.start()
    

    prob_gossip=0.75     
    port_list = [i for i in range(port_start, port_start+thread_count)]
    port_list.remove(port)
    Neighbours_port=random.sample(port_list,port_count)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1',port))
    server.listen()
    clientsocket, address = server.accept()
    Packet_string = json.loads(clientsocket.recv(1024).decode())
    clock = max(Packet_string["clock"], clock) + 1
    print(f"port {port} ↓ {Packet_string}\n")
    if port not in recieved_ports_list:
          recieved_ports_list.append(port)
           
    gossip= int((1-prob_gossip)*port_count)

    while len(list(set(recieved_ports_list))) < thread_count :
            if gossip==0:
                  final_neighbor_list= random.sample(Neighbours_port, k=1)
            else:
                  final_neighbor_list= random.sample(Neighbours_port, k=gossip)
            
            
            counter_loop = 0
            for member in round:
                  counter_loop+=1
                  for element in member:
                        if element == port:
                              if len(round)==counter_loop:
                                    round.append([])
                              for prt in final_neighbor_list:
                                    if prt not in round[counter_loop] and prt not in (item for sublist in round for item in sublist): 
                                          round[counter_loop].append(prt)


            for i in range(0,len(final_neighbor_list)):
                        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        if final_neighbor_list[i] not in recieved_ports_list:
                              message_packet = {
                                           "clock": Packet_string["clock"] + 1,
                                          "packet": Packet_string["packet"]
                                                }
                              c.connect(('127.0.0.1',final_neighbor_list[i]))
                              if final_neighbor_list[i] not in recieved_ports_list:
                                    c.send(bytes(json.dumps(message_packet).encode()))
                                    print(f"port {port} -----> {final_neighbor_list[i]} : {Packet_string}\n")            
    
for i in range(0,thread_count):
    t = threading.Thread(target=mesg , args=(i,port_start+i, NeiCout[i]))
    t.start()

#while True:
time.sleep(3)


Packet_string_old= input("Enter your Message: ") 
Packet_string={"clock": clock, "packet":Packet_string_old}
send_port= int(input(f"Which port do you want to send your message to? choose between {port_start}-{port_start+thread_count-1}: "))
list_temp = []
list_temp.append(send_port)
round.append(list_temp)
first_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
first_client.connect(('127.0.0.1',send_port))
first_client.send(bytes(json.dumps(Packet_string).encode()))


while len(list(set(recieved_ports_list))) < thread_count:
      continue
time.sleep(3)
print(f"operatin completed: {len(round)}")
