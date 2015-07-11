
from bt_server import BtServer
from gui import Gui
from pykeyboard import PyKeyboard
from pymouse import PyMouse
from threading import Thread
import time
import bluetooth
import sys
#import esky
import platform

sys.stderr = sys.stdout # py2exe log suppression
g = Gui()
k = PyKeyboard()
m = PyMouse()
socket = None


# if hasattr(sys,"frozen"):
#     system = platform.system()
#     url = "http://rewave.is-great.net/"
#     if (system == "Windows") : url = url + "windows"
#     if (system == "Linux") : url = url + "linux"
#     if (system == "Darwin") : url = url + "darwin" 
#     app = esky.Esky(sys.executable, url)
#     app.auto_update()


def start_server():
    '''
    Start the server, wait for connection and start the read function
    '''
    global bs, socket
    bs = BtServer(socket)
    bs.start()
    socket = bs.socket # save the newly created socket for later ref
    g.mark_connected()
    read_from_client(bs)


def read_from_client(bs):
    '''
    Read function continues until "exit" is read
    '''
    while True:
        try:
            command = bs.recv()
            control_keyboard(command)
            if command == "ping":
                g.mark_ping()

            if command == "exit":
                print("recv exit, breaking")
                break

            if "move_mouse" in command:
                command = command.split("-")
                try:
                    x = float(command[1])*g.screen_width
                    y = float(command[2])*g.screen_height
                    m.move(int(x), int(y))
                except ValueError as v:
                    # raised when data sent without much delay
                    pass

        except KeyboardInterrupt:
            break

        except bluetooth.btcommon.BluetoothError:
            #connection reset by peer
            break

    print('out of loop')
    g.mark_waiting()
    bs.close_connection()
    start_server()


def control_keyboard(command):
    try:
        print(command)
        k.tap_key(k.lookup_character_keycode(command))
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

terminate_server = Thread(target=terminate_server)
terminate_server.start()

g.start()
