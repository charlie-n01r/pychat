import yaml
import socket
import threading


def send_group_message(sender, message) -> None:
    pass

def client_handler(client: socket.socket) -> None:
    pass

def load_config(path: str) -> dict:
    with open(path) as file:
        return yaml.safe_load(file)

def listen(server: socket.socket, limit: int) -> None:
    while True:
        server.listen(limit)
        client, address = server.accept()
        threading.Thread(target=client_handler, args=(client)).start()


if __name__ == '__main__':
    config = load_config('config.yml')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['HOST'], config['PORT']))
    listen(server, config['CONNECTION_LIMIT'])
