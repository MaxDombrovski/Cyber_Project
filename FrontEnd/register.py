import tkinter
import threading
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import Path
import re


class Register_Window1(tkinter.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.geometry('1280x720')
        self.title('Register Screen')
        self.hats = ["FrontEnd/player_assets/TopHat.png", "FrontEnd/player_assets/Cap.png"]
        self.shirts = ["FrontEnd/player_assets/WhiteShirt.png", "FrontEnd/player_assets/Suit.png"]
        self.pants = ["FrontEnd/player_assets/Jeans.png", "FrontEnd/player_assets/Shorts.png"]
        self.shoes = ["FrontEnd/player_assets/Sneakers.png", "FrontEnd/player_assets/Crocs.png"]

        # nickname label
        Label(self,
              text='Nickname: ',
              font=('Calibri', 24)
              ).place(
            relx=.6,
            rely=.1,
            anchor=W
        )

        # nickname entry
        self.name = Entry(self)
        self.name.place(relx=.8, rely=.1, anchor=W)

        # email label
        Label(self,
              text='Email: ',
              font=('Calibri', 24)
              ).place(
            relx=.6,
            rely=.3,
            anchor=W
        )

        # email entry
        self.email = Entry(self)
        self.email.place(relx=.8, rely=.3, anchor=W)

        # password label
        Label(self,
              text='Password: ',
              font=('Calibri', 24)
              ).place(
            relx=.6,
            rely=.5,
            anchor=W
        )

        # password entry
        self.password = Entry(self)
        self.password.place(relx=.8, rely=.5, anchor=W)

        # hat label
        Label(self,
              text='Headwear: ',
              font=('Calibri', 24)
              ).place(
            relx=.3,
            rely=.1,
            anchor=W
        )

        # hat combo box
        self.combohat = ttk.Combobox(self, state='readonly', values=self.path_to_name(self.hats))
        self.combohat.set(self.path_to_name(self.hats)[0])
        self.combohat.place(relx=.45, rely=.1, anchor=W)

        # hat image
        self.combohat.bind('<<ComboboxSelected>>', self.image_update)

        # shirt label
        Label(self,
              text='Shirt: ',
              font=('Calibri', 24)
              ).place(
            relx=.3,
            rely=.3,
            anchor=W
        )

        # shirt combobox
        self.comboshirt = ttk.Combobox(self, state='readonly', values=self.path_to_name(self.shirts))
        self.comboshirt.set(self.path_to_name(self.shirts)[0])
        self.comboshirt.place(relx=.45, rely=.3, anchor=W)

        # shirt image
        self.comboshirt.bind('<<ComboboxSelected>>', self.image_update)

        # pants label
        Label(self,
              text='Pants: ',
              font=('Calibri', 24)
              ).place(
            relx=.3,
            rely=.5,
            anchor=W
        )

        # pants combobox
        self.combopants = ttk.Combobox(self, state='readonly', values=self.path_to_name(self.pants))
        self.combopants.set(self.path_to_name(self.pants)[0])
        self.combopants.place(relx=.45, rely=.5, anchor=W)

        # pants image
        self.combopants.bind('<<ComboboxSelected>>', self.image_update)

        # shoes label
        Label(self,
              text='Shoes: ',
              font=('Calibri', 24)
              ).place(
            relx=.3,
            rely=.7,
            anchor=W
        )

        # shoes combobox
        self.comboshoes = ttk.Combobox(self, state='readonly', values=self.path_to_name(self.shoes))
        self.comboshoes.set(self.path_to_name(self.shoes)[0])
        self.comboshoes.place(relx=.45, rely=.7, anchor=W)

        self.comboshoes.bind('<<ComboboxSelected>>', self.image_update)

        # accessory label
        Label(self,
              text='Accessory: ',
              font=('Calibri', 24)
              ).place(
            relx=.3,
            rely=.9,
            anchor=W
        )

        # submit button
        self.submit_button = Button(self,
               text='Submit',
               font=('Calibri', 18),
               width=35,
               command=self.handle_add_user
               )
        self.submit_button.place(
            relx=.6,
            rely=.7,
            anchor=W
        )

        # close button
        Button(self,
               text='Close',
               font=('Calibri', 18),
               width=35,
               command=self.close
               ).place(
            relx=.6,
            rely=.9,
            anchor=W
        )

    # image changer
    def image_update(self, evt):
        self.hat_image_path = Path("player_assets/" + self.combohat.get() + ".png")
        self.hat_img = ImageTk.PhotoImage(Image.open(self.hat_image_path))
        Label(self, image=self.hat_img).place(relx=.13, rely=.15, anchor=S)

        self.shirt_image_path = Path("player_assets/" + self.comboshirt.get() + ".png")
        self.shirt_img = ImageTk.PhotoImage(Image.open(self.shirt_image_path))
        Label(self, image=self.shirt_img).place(relx=.13, rely=.3, anchor=CENTER)

        self.pants_image_path = Path("player_assets/" + self.combopants.get() + ".png")
        self.pants_img = ImageTk.PhotoImage(Image.open(self.pants_image_path))
        Label(self, image=self.pants_img).place(relx=.13, rely=.45, anchor=N)

        self.shoes_image_path = Path("player_assets/" + self.comboshoes.get() + ".png")
        self.shoes_img = ImageTk.PhotoImage(Image.open(self.shoes_image_path))
        Label(self, image=self.shoes_img).place(relx=.13, rely=.85, anchor=S)

        # canvas1 = Canvas(self, width=1280, height=720)
        # canvas1.pack()
        # bg = canvas1.create_image(0, 0, anchor=NW, image=PhotoImage(file="player_assets/purple.png"))
        # canvas1.tag_lower(shoesL)

    # file path to file name substring
    def path_to_name(self, list):
        namelist = []
        for i in range(len(list)):
            namelist.append(list[i].split('/')[-1].split('.')[0])
        return namelist

    # submit thread
    def handle_add_user(self):
        self.client_handler = threading.Thread(target=self.submit, args=())
        self.client_handler.daemon = True
        self.client_handler.start()

    # submit button press
    def submit(self):
        arr = ["REGISTER", self.combohat.get(), self.comboshirt.get(), self.combopants.get(), self.comboshoes.get(), "None", self.name.get(), self.email.get(), self.password.get()]
        str_insert = ",".join(arr)

        if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', self.email.get()):
            self.submit_button.config(text='irrational email')
        else:

            self.parent.csocket.send(str_insert.encode())
            data = self.parent.csocket.recv(1024).decode()

            Label(self,
                  text=data,
                  font=('Arial', 12),
                  fg='green'
                  ).place(
                relx=.5,
                rely=0.1,
                anchor=CENTER)

    # close button press
    def close(self):
        self.parent.deiconify()  # show parent
        self.destroy()  # close and destroy this screen
