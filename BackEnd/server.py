import socket
import tcp_by_size
import hashlib
import threading
from tblAppearance import *
from tblUser import *

class Server:
    # establishing ip and port for server
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(10)

        self.user_counter = 0
        self.player_position_list = ["480, 360"] * 10
        self.message_list = [""] * 10
        self.appearance_list = [" ,TopHat,Suit,Shorts,Crocs"] * 10

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

            self.user_counter += 1
            print('Clients online: ', self.user_counter)
            threading.Thread(target=self.main_logic, args=(conn,)).start()

    def main_logic(self, conn):

        # constant loop
        while True:
            try:
                # presenting options over different commands
                # choice = conn.recv(1024).decode('utf-8')
                choice = tcp_by_size.recv_by_size(conn)
                print(choice)
                csplit = choice.split(",")

                if csplit[0] == "LOGIN" and len(csplit) == 3:
                    self.login(conn, csplit[1], csplit[2])
                elif csplit[0] == "REGISTER" and len(csplit) == 9:
                    self.register(conn, csplit[1], csplit[2], csplit[3], csplit[4], csplit[5], csplit[6], csplit[7], csplit[8])
                elif csplit[0] == "GAME" and len(csplit) == 1:
                    # conn.send(str(self.user_counter-1).encode('utf-8'))
                    tcp_by_size.send_with_size(conn, str(self.user_counter-1))

                    self.game_update(conn)
                else:
                    break
            except:
                print("Client Disconnected")
                self.user_counter -= 1
                self.player_position_list[self.playernumber] = "480, 360"
                self.message_list[self.playernumber] = ""
                self.appearance_list[self.playernumber] = " ,TopHat,Suit,Shorts,Crocs"
                print('Clients online: ', self.user_counter)
                break

        conn.close()

    def login(self, conn, email, password):
        email_hash = hashlib.sha256(email.encode()).hexdigest()
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if self.tbluser.check_by_email_password(email_hash, password_hash):
            # adding player appearance to the queue
            appearance_id = self.tbluser.get_appearance_id_by_email(email_hash)
            player_name = self.tbluser.get_name_by_email(email_hash)
            player_appearance = self.tblAppearance.get_items_by_id(appearance_id)

            player_appearance_list = list(player_appearance)
            player_appearance_list = player_appearance_list[:-1]
            player_appearance_list[0] = player_name
            player_appearance_string = ",".join(player_appearance_list)

            self.appearance_list[self.user_counter - 1] = player_appearance_string
            print(player_appearance_list)

            # server's answer
            # conn.send(b"true")
            tcp_by_size.send_with_size(conn, "true")
        else:
            # conn.send(b"false")
            tcp_by_size.send_with_size(conn, "false")

    def register(self, conn, hat, shirt, pants, shoes, accessories, name, email, password):
        try:
            email_hash = hashlib.sha256(email.encode()).hexdigest()
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            if not self.tbluser.check_by_email_password(email_hash, password_hash):
                appearanceid = self.tblAppearance.give_id_to_player(hat, shirt, pants, shoes, accessories)
                self.tbluser.insert_user(name, email_hash, password_hash, appearanceid, 0)
                # conn.send("registration successful".encode('utf-8'))
                tcp_by_size.send_with_size(conn, "registration successful")
            else:
                # conn.send("user already exists".encode('utf-8'))
                tcp_by_size.send_with_size(conn, "user already exists")
        except:
            conn.send("registration failed".encode('utf-8'))

    def game_update(self, conn):
        while True:
            # player_data = conn.recv(1024).decode('utf-8')
            player_data = tcp_by_size.recv_by_size(conn)
            player_data = player_data.split("$")

            self.playernumber = int(player_data[1])

            self.message_list[int(player_data[1])] = player_data[2]
            self.player_position_list[int(player_data[1])] = player_data[0]

            appearance_messages_and_position = "$".join(self.appearance_list) + "$" + "$".join(self.message_list) + "$" + "$".join(self.player_position_list)

            # conn.send(messages_and_position.encode('utf-8'))
            tcp_by_size.send_with_size(conn, appearance_messages_and_position)


s = Server('0.0.0.0', 1731)
