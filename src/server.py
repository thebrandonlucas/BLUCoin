from flask import Flask, jsonify, request
from uuid import uuid4
from blockchain import Blockchain
from node import Node
from wallet import Wallet
from transaction import Transaction
from block import Block
from helper import (
    read_blockchain,
    write_blockchain,
    read_nodes,
    write_nodes,
    get_port,
    compress,
)
from wallet_helper import read_wallet, write_wallet

app = Flask(__name__)

node_identifier = uuid4()

# Initialize the blockchain from DB file (or create new one)
blockchain = Blockchain()
blockchain.chain = read_blockchain()
blockchain.peers = read_nodes()

# TODO: load/write wallet to DB
node = Node(blockchain)

wallet = read_wallet(blockchain)

# write wallet if not saved already
write_wallet(wallet.privkey, "brandon")

node.add_account(wallet)
node.set_blockreward_pubkey(wallet.pubkey)

@app.route("/mine", methods=["GET"])
def mine():
    # Can't mine until we are saving node/wallet data

    block = node.mine()

    write_blockchain(blockchain.json_serialize()["chain"])

    # height = blockchain.get_height(block.hash())

    # Deserialize transactions to return as JSON from API
    # txs = block.transactions
    # coinbase_tx = {
    #     "sender": txs["coinbase"].sender.to_string().hex(),
    #     "recipient": txs["coinbase"].recipient.to_string().hex(),
    #     "amount": txs["coinbase"].amount,
    #     "signature": txs["coinbase"].signature,
    # }

    # regular_txs = [
    #     {
    #         "sender": tx.sender.to_string().hex(),
    #         "recipient": tx.recipient.to_string.hex(),
    #         "amount": tx.amount,
    #         "signature": tx.signature.to_string().hex(),
    #     }
    #     for tx in txs["regular"]
    # ]

    response = {
        "message": "New Block Mined!",
        # "height": height,
        "hash": block.hash(),
        # Unpack the remaining attributes of block (timestamp, previous_hash, proof, transactions)
        **block.json_serialize(),
    }

    return jsonify(response), 201


# @app.route("/transactions/send")
@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "blockchain": blockchain.json_serialize()["chain"],
        "mempool": blockchain.pending_transactions,
        "difficulty": blockchain.difficulty,
        "block_reward": blockchain.block_reward,
    }

    return jsonify(response), 200


@app.route("/consensus")
def consensus():
    """
    Function to reach consensus using the longest valid chain rule
    """

if __name__ == "__main__":
    port = get_port()
    app.run(host="0.0.0.0", port=port)
