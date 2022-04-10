from time import time
from hashlib import sha256
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