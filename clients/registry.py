"""
The registry that contains all available federated learning clients.

Having a registry of all available classes is convenient for retrieving an instance based
on a configuration at run-time.
"""
import logging
from collections import OrderedDict

from clients import (
    simple,
    adaptive_sync,
    adaptive_freezing,
    mistnet,
    scaffold,
    fednova,
    fedsarah,
    tempo,
)

from config import Config

registered_clients = OrderedDict([
    ('simple', simple.Client),
    ('adaptive_sync', adaptive_sync.Client),
    ('adaptive_freezing', adaptive_freezing.Client),
    ('mistnet', mistnet.Client),
    ('scaffold', scaffold.Client),
    ('fednova', fednova.Client),
    ('fedsarah', fedsarah.Client),
    ('tempo', tempo.Client),
])


def get():
    """Get an instance of the server."""
    if hasattr(Config().clients, 'type'):
        client_type = Config().clients.type
    else:
        client_type = Config().algorithm.type

    if client_type in registered_clients:
        logging.info("Client: %s", client_type)
        registered_client = registered_clients[client_type]()
    else:
        raise ValueError('No such client: {}'.format(client_type))

    return registered_client
