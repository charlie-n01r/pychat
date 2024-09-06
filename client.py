import yaml
import socket
import threading


def load_config(path: str) -> dict:
    with open(path) as file:
        return yaml.safe_load(file)


if __name__ == '__main__':
    config = load_config('config.yml')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((config['HOST'], config['PORT']))