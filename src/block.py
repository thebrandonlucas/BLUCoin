from time import time
from hashlib import sha256

from transaction import Transaction


class Block:
    def __init__(
        self,
        previous_hash=None,
        timestamp=time(),
        transactions=[],
        nonce=0,
    ) -> None:
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = {"coinbase": None, "regular": transactions}
        self.nonce = nonce

    def __str__(self) -> str:
        result = "Block:\n"
        result += f"\n\tCoinbase Transaction:\n\t\t{str(self.transactions['coinbase'])}"
        for i, tx in enumerate(self.transactions["regular"]):
            result += f"\n\tTransaction {i}:\n\t\t{str(tx)}"
        return result

    def hash(self):
        block_data = str(
            [self.previous_hash, self.timestamp, self.transactions, self.nonce]
        ).encode()
        return sha256(block_data).hexdigest()

    def json_serialize(self):
        coinbase_tx = self.transactions["coinbase"].json_serialize(coinbase=True)
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
        return Block(previous_hash, timestamp, transactions, proof)
