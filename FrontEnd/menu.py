import tkinter
from tkinter import *
from .register import Register_Window1
from .login import Login_Window1


class Menu(tkinter.Tk):
    def __init__(self, csocket=None):
        super().__init__()
        self.geometry('600x800')
        self.title('Menu')
        self.csocket = csocket

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

        self.attributes('-topmost', True)

    def open_register_window1(self):
        window = Register_Window1(self)
        window.grab_set()
        self.withdraw()

    def open_login_window1(self):
        window = Login_Window1(self)
        window.grab_set()
        self.withdraw()


if __name__ == "__main__":
    app = Menu()
    app.mainloop()
