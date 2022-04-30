from flask import Flask, jsonify, request
from uuid import uuid4
from blockchain.blockchain import Blockchain
from blockchain.node import Node
from wallet.wallet import Wallet
from blockchain.transaction import Transaction
from blockchain.block import Block
from server.server_helper import get_port
from server.file_helper import read_blockchain, write_blockchain, read_nodes, write_nodes
from wallet.wallet_helper import read_wallet, write_wallet

app = Flask(__name__)

node_identifier = uuid4()

# Initialize the blockchain from DB file (or create new one)
blockchain = read_blockchain()
node = Node(blockchain)

wallet = read_wallet(blockchain)
write_wallet(wallet.privkey, "Brandon LUcas")

node.add_account(wallet)
node.set_blockreward_pubkey(wallet.pubkey)


@app.route("/mine", methods=["GET"])
def mine():
    block = node.mine()

    write_blockchain(blockchain.json_serialize())

    response = {
        "message": "New Block Mined!",
        "hash": block.hash(),
        # Unpack the remaining attributes of block (timestamp, previous_hash, proof, transactions)
        **block.json_serialize(),
    }

    return jsonify(response), 201


@app.route("/chain", methods=["GET"])
def full_chain():
    return jsonify(blockchain.json_serialize()), 200


@app.route("/consensus", methods=["GET"])
def consensus():
    """
    Function to reach consensus using the longest valid chain rule
    """
    new_chain = blockchain.consensus()
    if new_chain:
        response = {
            "new_chain": True,
            "message": "Longer valid chain found in neighbor. Updated local chain.",
        }
        write_blockchain(new_chain)
    else:
        response = {
            "new_chain": False,
            "message": "Local chain was longest valid chain among peers. No updates made.",
        }

    return jsonify(response), 200

# TODO: list nodes

# FIXME: what to do if requested peer offline (when asking for it's chain)?
@app.route("/nodes/register", methods=["POST"])
def register_peer():
    values = request.get_json()
    peers = values["nodes"]
    blockchain.register_peers(peers)
    response = {
        "message": f"Successfully added {len(peers)} peers",
        "new_peers": peers,
    }
    return jsonify(response), 201


# Add wallet send() method to send money to peers

if __name__ == "__main__":
    port = get_port()
    app.run(host="0.0.0.0", port=port)
