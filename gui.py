#! /usr/bin/python

import tkinter
import threading
import time


class Gui(threading.Thread):

    def __init__(self):
        self.colors = {
            "green": "#8ef3c2",
            "blue": "#deeaf3",
            "gray_fg": "gray8",
            "gray_bg": "gray55",
            "orange": "#f6b26b",
            "white": "white"
        }

        self.stop_flag = False
        threading.Thread.__init__(self)

    def run(self):
        self.root = tkinter.Tk()
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
            fg="gray8"
        )

        self.message_box.pack(fill=tkinter.X)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        if not self.stop_flag:
            self.root.mainloop()

    def on_close(self):
        try:
            self.s.stop()
        except AttributeError as e:
            pass

        self.stop_flag = True
        self.root.destroy()

    def set_server(self, s):
        self.s = s

    def update_label(self, new_text, bg=None, fg=None):
        self.message_box.config(text=new_text)
        if bg:
            self.message_box.config(bg=self.colors[bg])
        if fg:
            self.message_box.config(fg=self.colors[fg])

    def mark_waiting(self):
        self.update_label("Waiting for connection", "blue", "gray_fg")

    def mark_connected(self):
        self.update_label("Connected", "green", "white")

    def mark_ping(self):
        self.update_label(":P", "orange", "white")
        time.sleep(0.5)
        self.mark_connected()
