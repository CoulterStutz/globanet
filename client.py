import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
client_name = 'us-n'  # The name of this client

print(f"\n{client_name}'s Console <3\n")

def encode_message(from_, to, request_type, request):
    message = {'From': from_, 'To': to, 'Request_Type': request_type, 'Request': request}
    return json.dumps(message).encode()

# Create a TCP/IP socket and connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Start a loop to listen for user input and send messages to the server
    while True:
        input_str = input('> ')

        # Parse the input into a message and send it to the server
        input_parts = input_str.split()
        if len(input_parts) < 2:
            print('Invalid input format. Please use: from to type command')
            continue

        from_, to, request_type = input_parts[:3]
        from_ = client_name
        request = ' '.join(input_parts[3:])
        message_data = encode_message(from_, to, request_type, request)
        s.sendall(message_data)


        # Wait for the server's response and decode it
        response_data = s.recv(1024)
        response = response_data.decode()

        # Check if the message is for this client
        response_message = json.loads(response)
        if response_message['To'] == client_name:
            None    # command parser
