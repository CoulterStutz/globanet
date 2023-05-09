import socket
import threading
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def handle_client(conn, addr):
    print(f'Connected by {addr}')

    while True:
        data = conn.recv(1024)
        if not data:
            break

        try:
            message = json.loads(data.decode())
            print(f'Received message: {message}')

            # Echo the message back to all connected clients
            for client_conn in clients:
                    client_conn.sendall(data)
                    print("sent message!")

        except json.JSONDecodeError:
            print('Received invalid JSON')

    conn.close()
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
