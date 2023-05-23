import socket
import re
from FrontEnd import menu


# def __init__(self):
#     self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     self.client_socket.connect(('127.0.0.1', 1731))
#     data = self.client_socket.recv(1024).decode()
#     print("data: " + data)


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        ask_ip = input("Enter server ip: ")
        if not re.fullmatch(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ask_ip):
            print("ip address inputted incorrectly")
        else:
            print("Waiting for connection")
            try:
                client_socket.connect((ask_ip, 1731))
                break
            except:
                print("Couldn't find ip address")

    print("Connection established")
    m = menu.Menu(client_socket)
    m.mainloop()
