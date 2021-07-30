import socket

def getHostIP():
    h_name = socket.gethostname()
    h_ip = socket.gethostbyname(h_name)
    return h_ip