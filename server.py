import datetime
import hashlib
import socket
import threading
import json
import boto3
from termcolor import colored

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

verify_chain_frequency = 100  # after x requests, the server will run a chain verification

clients = set()
approved_clients = set()

def get_chain_verification_frequency():
    return verify_chain_frequency


def set_chain_verification_frequency(chain_frequency: int):
    verify_chain_frequency = chain_frequency

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
            else:
                c += 1
        except IndexError:
            None
            # Return retry then have it start the process again

    if c == i:
        approved_clients.add(conn)
        conn.send("Logged In Successfully!\n".encode())
        print(f"{colored('Verified', 'green')} the identity of {client_name}:{addr}")
        broadcast_new_user(client_name)

def handle_client(conn, addr):
    print(f'Connected by {addr}\n')
    data = conn.recv(1024)
    d = data.decode().split()
    verify_login_hash(d[0], d[1], conn, addr)

    while True:
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
            print('Received invalid JSON')

    clients.remove(conn)
    print(f'Connection closed by {addr}')


# Create a TCP/IP socket and bind it to the port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)

    clients = set()

    while True:
        conn, addr = s.accept()
        clients.add(conn)

        # Start a new thread to handle the client connection
        threading.Thread(target=handle_client, args=(conn, addr)).start()
