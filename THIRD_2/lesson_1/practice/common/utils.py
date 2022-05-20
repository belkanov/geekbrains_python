import json
from socket import socket

from .variables import MAX_PACKAGE_LENGTH, DEFAULT_ENCODING
from .decors import log


@log
def get_message(client: socket):
    """

    """

    incoming_encoded_msg = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(incoming_encoded_msg, bytes):
        incoming_decoded_msg = incoming_encoded_msg.decode(DEFAULT_ENCODING)
        incoming_json_msg = json.loads(incoming_decoded_msg)
        if isinstance(incoming_json_msg, dict):
            return incoming_json_msg
        raise ValueError
    raise ValueError


@log
def send_message(socket: socket, message: dict):
    """

    """

    json_msg = json.dumps(message)
    outcoming_encoded_msg = json_msg.encode(DEFAULT_ENCODING)
    socket.send(outcoming_encoded_msg)

