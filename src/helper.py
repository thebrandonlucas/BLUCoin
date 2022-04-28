import json
import sys
import os


def get_port():
    """
    Gets the port number to use (for multiple nodes running on the same machine)
    Defaults to 5000, but user can bypass using system commands
    """
    if len(sys.argv) > 1:
        port = sys.argv[1]
        return port
    return 5000


def read_blockchain() -> object:
    """
    Read blockchain data from the saved file when coming back
    online. If blockchain file is unavailable, it creates it.

    :param filepath: <str> filepath (and name) to read from
    :return: <object> loaded chain data as a json object
    """
    if not os.path.isfile("../db/blockchain.json"):
        return []
    with open("../db/blockchain.json", "r") as file:
        chain = []
        json_chain = json.load(file)
        # for json_block in json_chain:
            # coinbase_tx = 
            # # TODO: convert TXs
            # regular_txs = [Transaction(tx[''])]
            
            # block = Block(
            #     previous_hash=json_block["previous_hash"],
            #     timestamp=json_block["timestamp"],
            #     transactions=json_block["transactions"],
            #     nonce=json_block["proof"],
            # )
            # chain.append(block)
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
    print("OS", os.getcwd())
    with open("../db/blockchain.json", "w") as file:
        json.dump(chain, file)


def write_nodes(data: object):
    """
    Write the peer node data to a file so that a node can safely go offline
    without losing all data

    :param data: <object> the data to write to file in JSON format
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

def compress(pubkey):
    """
    Convert pubkey to hex string in compressed format
    Read more: https://github.com/tlsfuzzer/python-ecdsa
    """
    return pubkey.to_string("compressed").hex()



