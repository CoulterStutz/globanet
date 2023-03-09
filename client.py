import os
import socket
import threading
import subprocess

import iterate

callsign = "[US-E]"

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the local machine name
host = socket.gethostname()

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
                        out = f'{callsign} --> {message_parsed}:{subprocess.check_output(message_parsed["command"])} IGNORE'
            except:
                None


# start a new thread to handle server messages
server_thread = threading.Thread(target=handle_server_messages)
server_thread.start()

while True:
    # read input from the user
    message = input(f"{callsign}@callsign:>>")
    message = f"{callsign} --> " + message
    print(message)
    client_socket.sendall(message.encode())
