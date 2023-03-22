import tkinter
from tkinter import *
from client import client
import socket
import threading
from register import Register_Window1
from login import Login_Window1


class menu(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x800')
        self.title('Menu')
        self.client = client

        # title label
        Label(self,
              text='MENU',
              font=('Calibri', 60)
              ).place(
            relx=.5,
            rely=.2,
            anchor=CENTER
        )

        # register button
        Button(self,
               text='Register',
               font=('Calibri', 36),
               command=self.open_register_window1
               ).place(
            relx=.5,
            rely=.4,
            anchor=CENTER
        )

        # login button
        Button(self,
               text='Login',
               font=('Calibri', 36),
               command=self.open_login_window1
               ).place(
            relx=.5,
            rely=.6,
            anchor=CENTER
        )

        # close button
        Button(self,
               text='Close',
               font=('Calibri', 24),
               fg='white',
               bg='red',
               command=self.destroy
               ).place(
            relx=.5,
            rely=.8,
            anchor=CENTER
        )

        self.handle_thread_socket()

    def open_register_window1(self):
        window = Register_Window1(self)
        window.grab_set()
        self.withdraw()

    def open_login_window1(self):
        window = Login_Window1(self)
        window.grab_set()
        self.withdraw()

    def handle_thread_socket(self):
        client_handler = threading.Thread(target=self.client, args=())
        client_handler.daemon = True
        client_handler.start()


if __name__ == "__main__":
    app = menu()
    app.mainloop()
