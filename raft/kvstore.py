# kvstore.py

# A networked Python dictionary

import msgpass

data = {}

def get(key):
    return data[key]

def set(key, value):
    data[key] = value

def delete(key):
    del data[key]

# put on the network (somehow)
from socket import *
import threading

def run_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock.bind(address)
    sock.listen(1)
    print(f"server running at {address}")
    while True:
        client, addr = sock.accept()
        # handle_client(client)  # <<<<CHANGE
        threading.Thread(target=handle_client, args=(client,)).start()

import pickle
def decode_request(msg):
    return pickle.loads(msg)

def encode_result(result):
    return pickle.dumps(result)

client_lock = threading.Lock()

def handle_client(client):
    while True:
        msg = msgpass.recv_message(client)
        method, args = decode_request(msg)
        print('request:', method, args)

        try:
            with client_lock:
                # guaranteed that only one thread at a time is in here
                if method == 'get':
                    result = get(*args)
                elif method == 'set':
                    set(*args)
                    result = "ok"
                elif method == "delete":
                    delete(*args)
                else:
                    raise RuntimeError(f"Bad method {method}")
        except:
            result = ("error", err)

        msgpass.send_message(client,
            encode_result(result)
            )

if __name__ == '__main__':
    run_server(('', 30000))


