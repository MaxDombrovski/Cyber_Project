import tkinter
import threading
from tkinter import *
from .main_lobby import Game


class Login_Window1(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry('400x300')
        self.title('Login Screen')

        # email label
        Label(self,
              text='Email: ',
              font=('Calibri', 24)
              ).place(
            relx=0,
            rely=0.2,
            anchor=W
        )

        # email entry
        self.email = Entry(self)
        self.email.place(relx=.5, rely=.2, anchor=CENTER)

        # password label
        Label(self,
              text='Password: ',
              font=('Calibri', 24)
              ).place(
            relx=0,
            rely=0.4,
            anchor=W
        )

        # password entry
        self.password = Entry(self)
        self.password.place(relx=.5, rely=.4, anchor=CENTER)

        # submit button
        Button(self,
               text='Submit',
               font=('Calibri', 18),
               command=self.handle_add_user
               ).place(
            relx=.5,
            rely=.6,
            anchor=CENTER
        )

        # close button
        Button(self,
               text='Back',
               font=('Calibri', 18),
               command=self.close
               ).place(
            relx=.5,
            rely=.8,
            anchor=CENTER
        )

    def open_main_lobby(self):
        self.parent.csocket.send(b"GAME")
        self.destroy()
        u = Game(self.parent.csocket)

    def close(self):
        self.parent.deiconify()  # show parent
        self.destroy()  # close and destroy this screen

    def handle_add_user(self):
        self.client_handler = threading.Thread(target=self.submit, args=())
        self.client_handler.daemon = True
        self.client_handler.start()

    def submit(self):
        arr = ["LOGIN", self.email.get(), self.password.get()]
        str_insert = ",".join(arr)

        self.parent.csocket.send(str_insert.encode())
        data = self.parent.csocket.recv(1024).decode()

        if data == "true":
            self.open_main_lobby()
        elif data == "false":
            Label(self,
                  text='Password or email have not been entered correctly',
                  font=('Arial', 12),
                  fg='red'
                  ).place(
                relx=.5,
                rely=0.1,
                anchor=CENTER)


