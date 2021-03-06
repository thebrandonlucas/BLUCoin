import json
import sys, os

# Get relative path to blockchain files
script_dir = os.path.dirname(__file__)
module_dir = os.path.join(script_dir, "..", "src")
sys.path.append(module_dir)

from blockchain import Blockchain


def read_blockchain() -> object:
    """
    Read blockchain data from the saved file when coming back
    online. If blockchain file is unavailable, it creates it.

    :param filepath: <str> filepath (and name) to read from
    :return: <object> loaded chain data as a json object
    """
    if not os.path.isfile("db/blockchain.json"):
        return Blockchain()
    with open("db/blockchain.json") as file:
        # FIXME: This doesn't deserialize "everything" i.e. the difficulty, peers, etc, just the chain itself
        json_chain = json.load(file)
        chain = Blockchain.json_deserialize(json_chain)
        return chain


def write_blockchain(chain: object):
    """
    Write the blockchain data to a file so that a node can safely go offline
    without losing all data

    :param data: <object> the data to write to file in JSON format
    :param filepath: <str> Type of data to write (either "blockchain" or "node")
    :returns: None
    """
    with open("db/blockchain.json", "w") as file:
        json.dump(chain, file)
