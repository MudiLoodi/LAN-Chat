import socket
from threading import Thread
from _thread import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostbyname("localhost")
port = 2004

active_connections = {}
addresses = {}

try:
    server_socket.bind((host, port))
except socket.error as err:
    print(f"Error: {err}")


def broadcast(msg, prefix=""):  # prefix is for name prefix.
    """Override default broadcast function"""
    for sock in active_connections:
        sock.send(str.encode(prefix, "utf8")+msg)


def client_thread(client_socket):
    """Worker thread for handling a single client connection."""

    name = client_socket.recv(1024).decode("utf8")
    welcome = "Welcome %s! Type -quit, if you want to disconnect." % name
    client_socket.send(str.encode(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(str.encode(msg))
    active_connections[client_socket] = name

    while True:
        msg = client_socket.recv(1024)
        if msg != str.encode("-quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client_socket.send(str.encode("> Disconnected...", "utf8"))
            client_socket.close()
            del active_connections[client_socket]
            broadcast(str.encode("%s has left the chat." % name, "utf8"))
            break


def accept_incoming_connections():
    """Sets up a thread for handling incoming connections"""

    while True:
        client, client_address = server_socket.accept()
        print("%s:%s has connected." % client_address)
        client.send(
            bytes("Welcome, please enter your username!", "utf8"))
        addresses[client] = client_address
        Thread(target=client_thread, args=(client,)).start()


if __name__ == "__main__":
    server_socket.listen(5)
    print("Waiting for connection...")
    incoming_connections_thread = Thread(target=accept_incoming_connections)
    incoming_connections_thread.start()
    incoming_connections_thread.join()
    server_socket.close()
