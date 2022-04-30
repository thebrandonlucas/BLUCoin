import json
from time import time
from hashlib import sha256

from transaction import Transaction


class Block:
    def __init__(
        self,
        previous_hash=None,
        timestamp=time(),
        transactions={"coinbase": None, "regular": []},
        nonce=0,
    ) -> None:
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce

    def __str__(self) -> str:
        return json.dumps(self.json_serialize())

    def hash(self):
        block_data = json.dumps(self.json_serialize()).encode()
        return sha256(block_data).hexdigest()

    def valid_proof(self, difficulty):
        """
        Determine whether a proof used in PoW is a valid difficulty
        """
        return self.hash()[:difficulty] == "0" * difficulty

    def json_serialize(self):
        coinbase_tx = (
            self.transactions["coinbase"].json_serialize()
            if self.transactions["coinbase"]
            else None
        )
        regular_txs = [tx.json_serialize() for tx in self.transactions["regular"]]
        return {
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": {"coinbase": coinbase_tx, "regular": regular_txs},
            "proof": self.nonce,
        }

    @staticmethod
    def json_deserialize(json_block):
        previous_hash = json_block["previous_hash"]
        timestamp = json_block["timestamp"]
        coinbase_tx = Transaction.json_deserialize(
            json_block["transactions"]["coinbase"]
        )
        regular_txs = [
            Transaction.json_deserialize(tx)
            for tx in json_block["transactions"]["regular"]
        ]
        transactions = {
            "coinbase": coinbase_tx,
            "regular": regular_txs,
        }
        proof = json_block["proof"]
        block = Block(previous_hash, timestamp, transactions, proof)
        return block
