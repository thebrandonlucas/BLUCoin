from ecdsa import VerifyingKey, SECP256k1
from flask import Flask, jsonify, request
from uuid import uuid4

import sys, os

# Get relative path to blockchain files
script_dir = os.path.dirname(__file__)
module_dir = os.path.join(script_dir, "..", "src/blockchain")
sys.path.append(module_dir)

from node import Node
from server_helper import get_port, compress
from file_helper import read_blockchain, write_blockchain
from wallet_helper import read_wallet, write_wallet
from transaction import Transaction

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


@app.route("/peers/list")
def list_peers():
    """
    List all the peers saved by the current node
    """
    response = {"peers": list(blockchain.peers)}
    return jsonify(response), 200


# FIXME: what to do if requested peer offline (when asking for it's chain)?
@app.route("/peers/register", methods=["POST"])
def register_peer():
    values = request.get_json()
    peers = values["peers"]
    blockchain.register_peers(peers)
    response = {
        "message": f"Successfully added {len(peers)} peers",
        "new_peers": peers,
    }
    return jsonify(response), 201


@app.route("/wallet/pubkey", methods=["GET"])
def get_pubkey():
    """
    Show the pubkey for the wallet associated with this node
    """
    response = {
        "pubkey": compress(wallet.pubkey),
        "nickname": wallet.nickname if wallet.nickname else "No Nickname Set",
    }
    return jsonify(response), 200


# Add wallet send() method to send money to peers
@app.route("/wallet/send", methods=["POST"])
def send():
    """
    request:
    {
        "recipient_pubkey": "0x324...",
        "amount": 20
    }
    """
    values = request.get_json()
    recipient_pubkey = VerifyingKey.from_string(
        bytearray.fromhex(values["recipient_pubkey"]), curve=SECP256k1
    )
    amount = values["amount"]
    # TODO: broadcast tx to other mempools of other miners (Instead of just ours)
    if wallet.send(recipient_pubkey, amount) is True:
        response = {"message": f"Sent {amount} BLU to {values['recipient_pubkey']}"}
    else:
        response = {
            "message": f"{compress(wallet.pubkey)} attempted to send {amount} but only had {wallet.verified_balance()} verified"
        }
    return jsonify(response), 201


# Add wallet balance(), unverified_balance(), verified_balance()
@app.route("/wallet/balance", methods=["GET"])
def balance():
    """
    Check the balance of a wallet
    """
    response = {
        "wallet": wallet.nickname if wallet.nickname else compress(wallet.pubkey),
        "total_balance": wallet.balance(),
    }
    return jsonify(response), 200

@app.route("/wallet/balance/unverified", methods=["GET"])
def unverified_balance():
    """
    Get balance of a wallet that's sitting in the mempool
    """
    response = {
        "wallet": wallet.nickname if wallet.nickname else compress(wallet.pubkey),
        "unverified_balance": wallet.unverified_balance(),
    }
    return jsonify(response), 200

@app.route("/wallet/balance/verified", methods=["GET"])
def verified_balance():
    """
    Get balance of a wallet that's confirmed on the blockchain
    """
    response = {
        "wallet": wallet.nickname if wallet.nickname else compress(wallet.pubkey),
        "verified_balance": wallet.verified_balance(),
    }
    return jsonify(response), 200

@app.route("/mempool", methods=["GET"])
def mempool():
    """
    Get the pending_transactions (mempool) for the local blockchain
    """
    pending_transactions = [
        tx.json_serialize() for tx in blockchain.pending_transactions
    ]
    response = {"pending_transactions": pending_transactions}
    return jsonify(response), 200


# @app.route("/wallet/verified_balance")

# @app.route("/wallet/unverified_balance")

if __name__ == "__main__":
    port = get_port()
    app.run(host="0.0.0.0", port=port)
