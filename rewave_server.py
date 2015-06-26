
from bt_server import BtServer
from gui import Gui
from pykeyboard import PyKeyboard
from threading import Thread
import time

g = Gui()
k = PyKeyboard()
bs = BtServer()

key_bindings = {
    'left': k.left_key,
    'right': k.right_key,
    'up': k.up_key,
    'down': k.down_key
}


def start_server():
    '''
    Start the server, wait for connection and start the read function
    '''
    global bs
    bs.start()
    g.mark_connected()
    read_from_client(bs)


def read_from_client(bs):
    '''
    Read function continues until "exit" is read
    '''
    try:
        command = bs.recv()
        control_keyboard(command)
        if command == "ping":
            g.mark_ping()

        if command == "exit":
            g.mark_waiting()
            bs.reset()

        else:
            read_from_client(bs)  # recursion

    except IOError:
        pass

    except KeyboardInterrupt:
        g.mark_waiting()
        bs.reset()


def control_keyboard(command):
    try:
        k.tap_key(key_bindings[command])
    except KeyError:
        pass


def terminate_server():
    '''
    Poll gui to see if it's closed, if yes, close the bt_server as well
    '''
    global bs, g
    while True:
        if g.is_closed():
            bs.stop()
            break
        else:
            time.sleep(1)

read_thread = Thread(target=start_server)
read_thread.start()

# terminate_server = Thread(target=terminate_server)
# terminate_server.start()

g.start()
