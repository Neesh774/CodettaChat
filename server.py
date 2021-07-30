from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

import getIP

def write_to_file(text):
    with open("logs.txt", "a") as f:
        logs = open("logs.txt", "a")
        f.write(text + "\n")
        logs.close()

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("SERVER:Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        write_to_file("%s:%s has started Codetta" % client_address)
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")[:10]
    welcome = 'WELCOME:Welcome %(name)s! If you ever want to quit, type {quit} to exit.  There are %(numOnline)s people online right now.' % {"name": name, "numOnline": len(clients)}
    client.send(bytes(welcome, "utf8"))
    write_to_file("%s has joined the chat!" % name)
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        try:
            msg = client.recv(BUFSIZ)
        except:
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            print("%s has disconnected" % name)
            write_to_file("%s has disconnected" % name)
            break
        if msg != bytes("{quit}", "utf8"):
            sendToAllButOne(msg, client, name+": ")


def broadcast(msg, prefix="SERVER:"):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
    write_to_file(prefix + msg.decode("utf8"))

def sendToAllButOne(msg, client, prefix="SERVER:"):
    for sock in clients:
        if(sock != client):
            sock.send(bytes(prefix, "utf8")+msg)
    write_to_file(prefix + msg.decode("utf8"))


clients = {}
addresses = {}
HOST = getIP.getHostIP()
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection at " + HOST + "...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()