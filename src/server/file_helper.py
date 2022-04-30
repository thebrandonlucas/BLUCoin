import json
import os
from blockchain.blockchain import Blockchain
from blockchain.block import Block


def read_blockchain() -> object:
    """
    Read blockchain data from the saved file when coming back
    online. If blockchain file is unavailable, it creates it.

    :param filepath: <str> filepath (and name) to read from
    :return: <object> loaded chain data as a json object
    """
    if not os.path.isfile("../db/blockchain.json"):
        return Blockchain()
    with open("../db/blockchain.json") as file:
        # FIXME: This doesn't deserialize "everything" i.e. the difficulty, peers, etc, just the chain itself
        json_chain = json.load(file)
        chain = Blockchain.json_deserialize(json_chain)
        return chain


def read_nodes() -> set:
    """
    Read peer nodes data from the saved file when coming back
    online.

    :return: <set> loaded peer nodes data as a set
    """
    if not os.path.isfile("./db/nodes.json"):
        return set()
    with open("../db/nodes.json", "r") as file:
        return set(json.load(file))


def write_blockchain(chain: object):
    """
    Write the blockchain data to a file so that a node can safely go offline
    without losing all data

    :param data: <object> the data to write to file in JSON format
    :param filepath: <str> Type of data to write (either "blockchain" or "node")
    :returns: None
    """
    with open("../db/blockchain.json", "w") as file:
        json.dump(chain, file)


def write_nodes(data):
    """
    Write the peer node data to a file so that a node can safely go offline
    without losing all data

    :param data: <array> the data to write to file in JSON format
    :param filepath: <str> Type of data to write (either "blockchain" or "node")
    :returns: None
    """
    with open("../db/nodes.json", "w") as file:
        json.dump(data, file)


def read_accounts():
    with open("../db/accounts.json") as file:
        return json.load(file)


def write_accounts(accounts):
    with open("../db/accounts.json") as file:
        json.dump(accounts, file)
