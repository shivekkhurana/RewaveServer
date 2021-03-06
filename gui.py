#! /usr/bin/python

import tkinter
import time


class Gui():

    def __init__(self):
        self.colors = {
            "green": "#8ef3c2",
            "blue": "#317cde",
            "gray_fg": "gray8",
            "gray_bg": "gray55",
            "orange": "#f6b26b",
            "white": "white"
        }
        self.closed = False # this is accessed in another thread to stop the bt_server when the window is closed

        self.root = tkinter.Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.tk.call('wm', 'iconphoto', self.root._w, tkinter.PhotoImage(file='images/rewave_app_icon.png'))
        self.root.resizable(0, 0)
        self.root.configure(background='white')
        self.root.title("Rewave Server")
        self.root.geometry('320x180')

        self.message_box = tkinter.Label(
            self.root,
            text="Waiting for connection",
            font=("Helvetica", 13),
            height=200,
            bg=self.colors["blue"],
            fg="white"
        )

        self.message_box.pack(fill=tkinter.X)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


    def start(self):
        self.root.mainloop()

    def on_close(self):
        self.root.destroy()
        self.closed = True

    def is_closed(self):
        return self.closed

    def update_label(self, new_text, bg=None, fg=None):
        self.message_box.config(text=new_text)
        if bg:
            self.message_box.config(bg=self.colors[bg])
        if fg:
            self.message_box.config(fg=self.colors[fg])

    def mark_waiting(self):
        self.update_label("Waiting for connection", "blue", "white")

    def mark_connected(self):
        self.update_label("Connected", "green", "white")

    def mark_ping(self):
        self.update_label(":P", "orange", "white")
        time.sleep(0.5)
        self.mark_connected()

    def mark_retrying(self):
        self.update_label("Cannot start server, retrying ... \n Make sure that bluetooth is available", "gray_bg", "gray_fg")