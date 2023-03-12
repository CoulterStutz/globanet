"""
PROGRAM NAME: Server.py
PROGRAM POURPOSE: To serve as the main socket for the clients to connect to and exchange data [see more below]
DATE WRITTEN: 3-8-23
PROGRAMMER: Coulter C. Stutz
"""

"""
How do I work, step by step visuals!

#1 [server.py] starts

#2 Clients connect on 

    [client.py(us-w)]       --->
    [client.py(us-e)]       --->
    [client.py(ca-c)]       --->
    [client.py(eu-frkf)]    --->
    [client.py(eu-stkh)]    --->    [server.py]
    [client.py(ap-mb)]      --->
    [client.py(ap-jp)]      --->
    [client.py(ap-sdy)]     --->

#3 Clients exchange info
    US-W to AS-JPN
    #1 [US-W] --> [Server] US-W SENDS TO SERVER
    #2 [ALL]  <-- [Server] SERVER BEAMS TO ALL
    #3 [AS-JP] --> [US-W]  AS-JP PICKS REQUEST UP

"""

import socket
import threading
import boto3

# list of connected client sockets
client_sockets = []

# function for handling a client connection
def handle_client(client_socket, client_address):
    print("New connection from: ", client_address)
    client_sockets.append(client_socket)

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode()
        print("Received message from {}: {}".format(client_address, message))

        for sock in client_sockets:
            sock.sendall(message.encode())

    client_sockets.remove(client_socket)
    print("Closing connection with: ", client_address)
    client_socket.close()

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the local machine name
host = "0.0.0.0"

# bind the socket to a public host, and a well-known port
server_socket.bind((host, 8000))

# set the maximum number of queued connections
server_socket.listen(5)

print("Server listening on {}:{}".format(host, 8000))

while True:
    # wait for a client connection
    client_socket, client_address = server_socket.accept()

    # start a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
