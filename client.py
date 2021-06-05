import socket
from threading import Thread


def receive():
    while True:
        msg = client_socket.recv(1024).decode("utf8")
        if msg == "-quit":
            client_socket.close()
            break
        if not msg:
            break
        print(msg)


def send():
    while True:
        msg = input("> ")
        client_socket.send(str.encode(msg, "utf8"))
        if msg == "-quit":
            break


host = socket.gethostbyname("localhost")
port = 2004

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

receive_thread = Thread(target=receive)
send_thread = Thread(target=send)
receive_thread.start()
send_thread.start()
receive_thread.join()
send_thread.join()
