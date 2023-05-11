import socket


class client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 1731))
        data = self.client_socket.recv(1024).decode()
        print("data: " + data)


u = client()
