"""
PROGRAM NAME: client.py
PROGRAM POURPOSE: To serve as the client of the global network
DATE WRITTEN: 5/10/23
Programmer: Coulter C. Stutz
"""

import socket, select, json
import os, sys, datetime
import hashlib
import threading

HOST = '127.0.0.1'
PORT = 65432
debug = False

client_name = str()
data_file = str()
peer_type = str()
host_peer_explorer = bool()
peer_pass = str()

if debug == True:
    try:
        client_name = sys.argv[1]
    except IndexError:
        None
else:
    config = json.loads(open("peer_information.json", "r").read())
    client_name = config["PeerName"]
    peer_type = config["PeerType"]
    host_peer_explorer = config["HostPeerExplorer"]
    peer_pass = config["PeerPass"]
    data_file = config["DataFile"]


def generate_login_hash():
    h = '-'.join(
        [str(datetime.datetime.now().month), str(datetime.datetime.now().day), str(datetime.datetime.now().hour),
         str(datetime.datetime.now().minute), client_name, peer_pass])
    return hashlib.sha256(h.encode()).digest()


login_hash = generate_login_hash()

def encode_message(from_, to, request_type, request):
    message = {'From': from_, 'To': to, 'Request_Type': request_type, 'Request': request}
    return json.dumps(message).encode()

def log(message):
    with open(data_file, 'a') as f:
        log_str = f"\n{message['From']} --> {message['To']}: {message['Request_Type']} {message['Request']}"
        f.write(f"{datetime.datetime.now()}: {log_str}\n")
        print(log_str)


def handle_server_messages():
    response_data = s.recv(1024)
    response = response_data.decode()
    print(response)

    response_message = json.loads(response)

    if response_message['From'] == "SERVER":
        if response_message['To'] == client_name or response_message['To'] == "all":
            if response_message['Request_Type'] == "welcome":
                print(f"{response_message['Request']} has successfully connected to the node")

    if response_message['To'] == client_name or response_message['To'] == "all":
        if response_message['Request_Type'] == "echo":
            print(response_message['Request'])
        elif response_message['Request_Type'] == "cmd":
            os.system(response_message['Request'])
            log(response_message)
        elif response_message['Request_Type'] == "areyouawake":
            if response_message['Request'] == client_name or response_message['To'] == "all":
                conn.send(encode_message(client_name, "all", "response", "Awake!"))
                log(response_message)
            else:
                log(response_message)
        else:
            log(response_message)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    print(f"{client_name}'s Console <3")
    s.send(f'{client_name} {login_hash}'.encode())
    print(login_hash)
    response_data = s.recv(1024)
    response = response_data.decode()

    if response == "Failed To Login: Invalid Hash":
        exit(1)
    elif response == "Retry":
        print("Reattempting Verification")
        s.send(f'{client_name} {login_hash}'.encode())
        print(login_hash)
        response_data = s.recv(1024)
        response = response_data.decode()
    else:
        print(response)

    inputs = [s]

    server_thread = threading.Thread(target=handle_server_messages)
    server_thread.start()

    while True:
        input_str = input('>> ')
        input_parts = input_str.split()
        if len(input_parts) < 2:
            print('Invalid input format. Please use: from to type command')
            continue

        from_, to, request_type = input_parts[:3]
        from_ = client_name
        request = ' '.join(input_parts[3:])
        message_data = encode_message(from_, to, request_type, request)
        s.sendall(message_data)
