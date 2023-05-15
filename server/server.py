"""
PROGRAM NAME: server.py
PROGRAM POURPOSE: to act as a server for the network
DATE WRITTEN: 5/10/23
PROGRAMMER:
"""


import datetime
import hashlib
import socket
import threading
import json
import peer_management as pm
from termcolor import colored

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

verify_chain_frequency = 100  # after x requests, the server will run a chain verification
allow_message_passthrough = True

clients = set()
approved_clients = set()
connected_clients = []
total_requests = []

def get_chain_verification_frequency():
    return verify_chain_frequency

def set_chain_verification_frequency(chain_frequency: int):
    verify_chain_frequency = chain_frequency

def allow_messages(allow_messages:bool):
    allow_message_passthrough = allow_messages

def encode_message(from_, to, request_type, request):
    message = {'From': from_, 'To': to, 'Request_Type': request_type, 'Request': request}
    return json.dumps(message).encode()

def broadcast_new_user(client_name):
    for client_conn in approved_clients:
        conn.send(encode_message("SERVER", "all", "welcome", client_name))


def verify_login_hash(client_name, hash, conn, addr):
    i = 0  # counter for hash verification
    c = 0  # counter for times the hash matched
    peer_pass = json.loads(open("server_config.json", "r").read())["PeerSecurity"]["us-w"]

    h = '-'.join(
        [str(datetime.datetime.now().month), str(datetime.datetime.now().day), str(datetime.datetime.now().hour),
         str(datetime.datetime.now().minute), client_name, peer_pass])
    dh = str(hashlib.sha256(h.encode()).digest())

    print(f"Verifying identity of {client_name}:{addr}")

    print(dh, hash)

    for x in range(1, len(dh)):
        i += 1
        try:
            if dh[x] != hash[i]:
                conn.send("Failed To Login: Invalid Hash\n".encode())
                print(f"Verifying the identity of {client_name}:{addr} {colored('FAILED', 'red')}")
                conn.close()
                return "Failed"
            else:
                c += 1
        except IndexError:
            return "Retry"

    if c == i:
        if client_name not in connected_clients:
            approved_clients.add(conn)
            connected_clients.append(client_name)
            conn.send("Logged In Successfully!\n".encode())
            print(f"{colored('Verified', 'green')} the identity of {client_name}:{addr}")
            broadcast_new_user(client_name)
            return True
        else:
            print(f"{colored('Denied', 'red')} the identity of {client_name}:{addr}, because {client_name} is already logged in")
            conn.send("Client is already logged in\n".encode())

def handle_client(conn, addr):
    print(f'Connected by {addr}\n')
    data = conn.recv(1024)
    d = data.decode().split()

    verify = verify_login_hash(d[0], d[1], conn, addr)

    if verify == "Retry":
        conn.send("Retry".encode())
        verify_login_hash(d[0], d[1], conn, addr)

    while True:
        if allow_message_passthrough:
            data = conn.recv(1024)
            if not data:
                break

            try:
                message = json.loads(data.decode())
                print(f"New Request | {message}")

                # Echo the message back to all connected clients
                for client_conn in approved_clients:
                    client_conn.sendall(data)

            except json.JSONDecodeError:
                None

    clients.remove(conn)
    approved_clients.remove(conn)
    print(f'Connection closed by {addr}')


# Create a TCP/IP socket and bind it to the port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print(f"Socket Binded to {HOST}:{PORT}")
    s.listen(5)

    clients = set()

    while True:
        conn, addr = s.accept()
        clients.add(conn)

        # Start a new thread to handle the client connection
        threading.Thread(target=handle_client, args=(conn, addr)).start()
