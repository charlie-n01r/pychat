import os
import yaml
import socket
import threading
from datetime import datetime


def message_handler(client: socket.socket, username: str) -> None:
    while True:
        message = client.recv(2048).decode()
        if message:
            timestamp = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
            payload = f'{username}::{message}::{timestamp}'
            send_group_message(payload)

def send_private_message(payload: str, client: socket.socket) -> None:
    client.sendall(payload.encode())

def send_group_message(payload: str, active_clients: list[tuple[str, socket.socket]]) -> None:
    for client in active_clients:
        send_private_message(payload, client[1])

def client_handler(client: socket.socket, active_clients: list) -> None:
    while True:
        username = client.recv(2048).decode()
        if username:
            active_clients.append((username, client))
            break
        else:
            pass
    
    threading.Thread(target=message_handler, args=(client, username)).start()

def listen(server: socket.socket, limit: int, active_clients: list[tuple[str, socket.socket]]) -> None:
    while True:
        server.listen(limit)
        client, address = server.accept()
        threading.Thread(target=client_handler, args=(client, active_clients)).start()

def load_config(path: str) -> dict:
    with open(path) as file:
        return yaml.safe_load(file)


if __name__ == '__main__':
    config = load_config('config.yml')
    active_clients = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['HOST'], config['PORT']))
    listen(server, config['CONNECTION_LIMIT'], active_clients)
