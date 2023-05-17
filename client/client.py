"""
PROGRAM NAME: client.py
PROGRAM POURPOSE: To serve as the client of the global network
DATE WRITTEN: 5/10/23
Programmer: Coulter C. Stutz
"""

import socket, select, json
import os, sys, datetime
import hashlib, threading
from random import random
import boto3, botocore
import references

HOST = '18.144.176.16'
PORT = 65432
debug = False

client_name = str()
data_file = str()
peer_type = str()
host_peer_explorer = bool()
peer_pass = str()
aws_region = ''

client_names_connected = []

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

if client_name == "us-w":
    aws_region = "us-west-2"
elif client_name == "us-e":
    aws_region = "us-east-2"
elif client_name == "ca-c":
    aws_region = "ca-central-1"
elif client_name == "eu-frnk":
    aws_region == "eu-central-1"
elif client_name == "eu-stkh":
    aws_region == "eu-north-1"
elif client_name == "as-mumb":
    aws_region == "ap-south-1"
elif client_name == "as-jpn":
    aws_region = "ap-northeast-1"
elif client_name == "as-syd":
    aws_region = "ap-southeast-2"
elif client_name == "sa-e":
    aws_region = "sa-east-1"

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
        log_str = f"{message['From']} --> {message['To']}: {message['Request_Type']} {message['Request']}"
        f.write(f"{datetime.datetime.now()}: {log_str}\n")
        print(log_str)


def aws_translate_text(from_lang, to_lang, message):
    translate = boto3.client("translate", region_name=aws_region)
    try:
        from_lang = from_lang.upper()
        to_lang = to_lang.upper()
        aws_response = translate.translate_text(
            Text=message.strip('"'),
            SourceLanguageCode=from_lang,
            TargetLanguageCode=to_lang.strip(),
            Settings={
                'Formality': 'INFORMAL',
                'Profanity': 'MASK'
            }
        )
        return aws_response
    except botocore.errorfactory.UnsupportedLanguagePairException:
        return False

def detect_language(message):
    comprehend = boto3.client('comprehend', region_name=aws_region)
    aws_response = comprehend.detect_dominant_language(
        Text=message
    )
    return aws_response

def handle_server_messages():
    while True:
        response_data = s.recv(1024)
        response = response_data.decode()

        try:
            response_message = json.loads(response)

            if response_message['From'] == "SERVER":
                if response_message['To'] == client_name or response_message['To'] == "all":
                    if response_message['Request_Type'] == "welcome":
                        print(f"{response_message['Request']} has successfully connected to the node")

            if response_message['To'] == client_name or response_message['To'] == "all":
                if response_message['Request_Type'] == "echo":
                    print(response_message['Request'])
                    log(response_message)
                elif response_message['Request_Type'] == "cmd":
                    os.system(response_message['Request'])
                    log(response_message)
                elif response_message['Request_Type'] == "areyouawake":
                    if response_message['Request'] == client_name or response_message['To'] == "all":
                        s.send(encode_message(client_name, "all", "response", "Awake!"))
                        log(response_message)
                    else:
                        log(response_message)
                elif response_message['Request_Type'] == "translate":
                    lang_from = response_message['Request'].split(",")[0][1:]
                    lang_to = response_message['Request'].split(",")[1]
                    message = response_message['Request'].split(",")[2][:-1].strip()

                    out = aws_translate_text(lang_from, lang_to, message)
                    if out == False:
                        s.send(encode_message(client_name, response_message["From"], "response",
                                              "Error! One of the languages are invalid."))
                    else:
                        s.send(encode_message(client_name, response_message["From"], "response", out['TranslatedText']))
                    log(response_message)
                elif response_message['Request_Type'] == "detect-language":
                    o = str()
                    out = detect_language(response_message['Request'])
                    for x in out["Languages"]:
                        o = o + f'{x["LanguageCode"]}: {x["Score"]}% '
                    log(response_message)
                    s.send(encode_message(client_name, response_message["From"], "response", o))
                elif response_message["Request_Type"] == "response":
                    log(response_message)
                else:
                    log(response_message)
            else:
                log(response_message)
        except json.decoder.JSONDecodeError:
            None


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    print(f"{client_name}'s Console <3")
    s.send(f'{client_name} {login_hash}'.encode())
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
    elif response == "Client is already logged in\n":
        exit(1)
    else:
        print(response)

    inputs = [s]

    server_thread = threading.Thread(target=handle_server_messages)
    server_thread.start()

    while True:
        input_str = input(f'{client_name}>> ')
        input_parts = input_str.split()
        if len(input_parts) < 2:
            print('Invalid input format. Please use: from to type command')
            continue
        else:
            from_, to, request_type = input_parts[:3]
            from_ = client_name
            request = ' '.join(input_parts[3:])
            message_data = encode_message(from_, to, request_type, request)
            s.sendall(message_data)
