from socket import socket, AF_INET, SOCK_DGRAM
sock = False

def make_sock(port):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', port)) # bind to all interfaces/addresses by default
    return sock

def get_data(port):
    global sock
    if not sock:
        sock = make_sock(port)
    packet = sock.recv(1024)
    exploded = [float(val) for val in packet.split(',')]
    return exploded
