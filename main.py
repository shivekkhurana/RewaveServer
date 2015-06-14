#! /usr/bin/python

import bt_server
import gui
import threading

from pykeyboard import PyKeyboard
from time import sleep


k = PyKeyboard()

key_bindings = {
    'left': k.left_key,
    'right': k.right_key,
    'up': k.up_key,
    'down': k.down_key
}


class ControlThread(threading.Thread):

    def __init__(self, g):
        self.g = g
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        while True:
            s = bt_server.BtServer()
            g = self.g
            g.set_server(s)
            try:
                g.mark_waiting()
            except AttributeError as e:
                # this can happen if mark_waiting is called before gui's run has
                # executed on another thread
                pass
            s.start()
            g.mark_connected()

            while True:
                try:
                    data = s.recv()
                    s.send(data)  # echo
                    print(data)
                    if data == "exit":
                        break
                    if data == "ping":
                        g.mark_ping()
                    try:
                        k.tap_key(key_bindings[data])
                    except KeyError:
                        pass
                    sleep(0.0006)

                except IOError:
                    pass

                except KeyboardInterrupt:
                    break


def main():
    g = gui.Gui()
    g.start()
    control_thread = ControlThread(g)
    control_thread.start()
    g.join()
    print("Fin")

if __name__ == '__main__':
    main()
