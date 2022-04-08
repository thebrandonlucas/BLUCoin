# Create a blockchain.
# A blockchain is a collection of records organized into chunks called blocks
# that are linked together using cryptography.

# A blockchain contains:
#  1 - A cryptographic hash of the previous block
#  2 - A timestamp
#  3 - Transaction data (in the form of a Merkle Tree)

# The usefulness of blockchains comes from:
# 1 - Publicly distributed ledger known to everyone
# 2 - Highly tamper resistant, changing one block makes all the subsequent blocks invalid

# Layers of blockchain:
# 1 - infrastructure (hardware)
# 2 - Networking (node discovery, information propagation, verification)
# 3 - Consensus (Proof of Work)
# 4 - data (Blocks & Transactions)
# 5 - Application (Smart Contracts)

from time import time
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1


class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 0x0

    def __str__(self):
        result = f"Blucoin Blockchain:\n\tDifficulty: {self.difficulty}"
        result += "\n\tPending Transactions:\n"
        for i, tx in enumerate(self.pending_transactions):
            result += f"\n\t\t- Transaction {i}:\n\t\t\t{str(tx)}"
        result += "\n\tBlocks:\n"
        for i, block in enumerate(self.chain):
            result += f"{i} {str(block)}"
        return result

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, winning_nonce=0x0):
        previous_hash = self.get_latest_block().hash()
        new_block = Block(
            previous_hash, time(), self.pending_transactions, winning_nonce
        )
        self.chain.append(new_block)
        self.pending_transactions = []


class Block:
    def __init__(
        self,
        previous_hash=None,
        timestamp=time(),
        transactions=[],
        winning_nonce=0x0,
    ) -> None:
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions

    def __str__(self) -> str:
        result = "Block:\n"
        for i, tx in enumerate(self.transactions):
            result += f"\n\tTransaction {i}:\n\t\t{str(tx)}"
        return result

    def hash(self):
        block_data = [self.previous_hash, self.timestamp, self.pending_transactions]
        return sha256(bytes(block_data)).hexdigest()


class Transaction:
    def __init__(self, sender, recipient, amount, signature=None) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def __str__(self) -> str:
        return f"TX: ({self.amount} Blu FROM sender: {self.sender.to_der().hex()} -> recipient: {self.recipient.to_der().hex()}), SIGNATURE: {self.signature}"


class Wallet:
    def __init__(self, privkey=None) -> None:
        if not privkey:
            self.privkey = SigningKey.generate(curve=SECP256k1)
            self.pubkey = self.privkey.verifying_key
        # TODO: what if user provides their own privkey?

    def send(self, recipient, amount, blockchain):
        # To send, we need to:
        # 1 - Create a transaction
        # 2 - Sign the transaction
        # 3 - Add to pool of pending transactions
        tx = Transaction(self.pubkey, recipient, amount)
        signature = self.sign(tx)
        tx.signature = signature
        blockchain.pending_transactions.append(tx)

    def sign(self, transaction):
        # In this case, the "message" is the bytes of our transaction
        signature = self.privkey.sign(str(transaction).encode())
        return signature

    def verify(self, signature, transaction):
        return self.pubkey.verify(signature, transaction)

    def unverified_balance(self, blockchain):
        # Unverified balance are the unverified transactions in pending_transactions
        unverified_balance = 0
        for tx in blockchain.pending_transactions:
            if tx.recipient == self.pubkey:
                unverified_balance += tx.amount
        return unverified_balance

    def verified_balance(self, blockchain):
        # These are transactions that have been included in the blockchain
        verified_balance = 0
        for block in blockchain.chain:
            for tx in block.transactions:
                if tx.recipient == self.pubkey:
                    verified_balance += tx.amount
        return verified_balance

    def balance(self, blockchain):
        # loop thru blockchain and add up tx's sent to account
        # (assuming no coinbase tx's)
        return self.verified_balance(blockchain) + self.unverified_balance(blockchain)
