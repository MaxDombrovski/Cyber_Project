import socket
import threading
from tblAppearance import *
from tblUser import *

class Server:
    # establishing ip and port for server
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(10)
        self.tbluser = tblUser()
        self.tblAppearance = tblAppearance()
        self.running = True
        self.wait_new_clients()
        # threading.Thread(target=self.wait_new_clients(), daemon=True).start()

    # waiting for new clients
    def wait_new_clients(self):
        while self.running:
            conn, addr = self.sock.accept()
            print('connected:', addr)
            conn.send("server connected".encode('utf-8'))
            threading.Thread(target=self.main_logic(conn,)).start()
            threading.Thread()

    def main_logic(self, conn):

        # constant loop
        while True:
            try:
                # presenting options over different commands
                choice = conn.recv(1024).decode('utf-8')
                csplit = choice.split(",")

                if csplit[0] == "LOGIN" and len(csplit) == 3:
                    self.login(conn, csplit[1], csplit[2])
                elif csplit[0] == "REGISTER" and len(csplit) == 9:
                    self.register(conn, csplit[1], csplit[2], csplit[3], csplit[4], csplit[5], csplit[6], csplit[7], csplit[8])
                else:
                    break
            except:
                print("Client Disconnected")
                break

        conn.close()

    def login(self, conn, email, password):
        if self.tbluser.check_by_email_password(email, password):
            conn.send("true".encode('utf-8'))
        conn.send("false".encode('utf-8'))

    def register(self, conn, hat, shirt, pants, shoes, accessories, name, email, password):
        try:
            if not self.tbluser.check_by_email_password(email, password):
                appearanceid = self.tblAppearance.give_id_to_player(hat, shirt, pants, shoes, accessories)
                self.tbluser.insert_user(name, email, password, appearanceid, 0)
                conn.send("registration successful".encode('utf-8'))
            else:
                conn.send("user already exists".encode('utf-8'))
        except:
            conn.send("registration failed".encode('utf-8'))


s = Server('0.0.0.0', 1731)
