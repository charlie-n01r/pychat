import os
import yaml
import socket
import logging
import threading
from datetime import datetime


def message_handler(client: socket.socket, username: str, active_clients: list[tuple[str, socket.socket]]) -> None:
    while True:
        message = client.recv(2048).decode()
        if message:
            timestamp = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
            payload = f'{timestamp}::{username}::{message}'
            send_group_message(payload, active_clients)
        else:
            logging.warning(f"Unable to process the message received from client '{client}'.")

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
            send_group_message(f"!> {username} is online!\n", active_clients)
            break
        else:
            logging.warning(f"Unable to process the information received from client '{client}'.")
    
    threading.Thread(target=message_handler, args=(client, username, active_clients)).start()

def listen(server: socket.socket, limit: int, active_clients: list[tuple[str, socket.socket]]) -> None:
    while True:
        server.listen(limit)
        client, address = server.accept()
        logging.info(f"Accepted connection to client '{client}' on address '{address}'.")
        threading.Thread(target=client_handler, args=(client, active_clients)).start()

def init_logging() -> None:
    log_dir = 'logs/server'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(filename=f'{log_dir}/log_{datetime.now()}.log', force=True,
                        level=logging.DEBUG, format='%(asctime)s::%(levelname)s - %(message)s'
    )

def load_config(path: str) -> dict:
    with open(path) as file:
        logging.info(f"Loading configuration parameters from '{path}'.")
        return yaml.safe_load(file)


if __name__ == '__main__':
    init_logging()
    config = load_config('config.yml')
    active_clients = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['HOST'], config['PORT']))
    logging.info(f"Server bound. Listening on {config['HOST']}:{config['PORT']}.")
    listen(server, config['CONNECTION_LIMIT'], active_clients)
