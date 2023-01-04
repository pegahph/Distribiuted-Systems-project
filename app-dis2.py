import socket 

host='192.168.10.254'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.10.1', 55555))

client.send("salam".encode())










