
from bt_server import BtServer
from gui import Gui
from pykeyboard import PyKeyboard
from threading import Thread

g = Gui()

k = PyKeyboard()
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
    bs = BtServer()
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
            bs.stop()

        else:
            read_from_client(bs)  # recursion

    except IOError:
        pass

    except KeyboardInterrupt:
        g.mark_waiting()
        bs.stop()


def start_server_perpetually():
    '''
    Keep on restarting the server after read completes
    '''
    while True:
        start_server()


def control_keyboard(command):
    try:
        k.tap_key(key_bindings[command])
    except KeyError:
        pass


read_thread = Thread(target=start_server_perpetually)
read_thread.start()
g.start()