import random
from gossip import Gossip

def main():
    host = 'localhost'
    connected_nodes = random.choices(node, weights=10, k=1)

    for port in range(5000,6001):
        node = Gossip(host, port, connected_nodes)
    

if __name__ == '__main__':
    main()