import os
import yaml
import socket
import logging
import threading
from datetime import datetime


def receive_message(client: socket.socket) -> None:
    while True:
        payload = client.recv(2048).decode()
        if payload:
            if payload.startswith('!>'):
                print(payload)
            else:
                timestamp, username, message = payload.split('::')
                print(f'{timestamp}  {username}: {message}', end='\n>> ')
        else:
            logging.warning(f"Unable to process the message received from client '{client}'.")

def send_message(client: socket.socket) -> None:
    while True:
        message = input('>> ')
        if message:
            if message == 'logout':
                client.close()
                exit(0)
            client.sendall(message.encode())
        else:
            print('Empty message')
            exit(1)

def server_link(client: socket.socket) -> None:
    username = input('Log in: ')
    if username:
        client.sendall(username.encode())
        threading.Thread(target=receive_message, args=(client, )).start()
        send_message(client)
    else:
        logging.error('Unable to log in!')
        exit(1)

def init_logging() -> None:
    log_dir = 'logs/client'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(filename=f'{log_dir}/log_{datetime.now()}.log', force=True,
                        level=logging.DEBUG, format='%(asctime)s::%(levelname)s - %(message)s'
    )

def load_config(path: str) -> dict:
    with open(path) as file:
        return yaml.safe_load(file)


if __name__ == '__main__':
    init_logging()
    config = load_config('config.yml')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((config['HOST'], config['PORT']))
    server_link(client)