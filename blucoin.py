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

# Mining and Consensus/Proof of work

# Mining is the process of looking for a valid "proof" of a miner discovering
# a number below the "target", which is a SHA256 number with a certain number of 0's prepended
# interpreted in little endian

from time import time
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1
import random


class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        self.pending_transactions = []
        # The number of prepended zeroes to the 256 bit target number
        self.difficulty = 5
        self.block_reward = 50

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
        if len(self.chain):
            return self.chain[-1]
        # Genesis block?
        return Block()

    def add_block(self, block, node):
        # Check the block hash for proof of work
        if block.hash()[: self.difficulty] <= "0" * self.difficulty:
            self.chain.append(block)
            self.pending_transactions = []
            print(f"Block {block.hash()} added!")
            print(f"Rewarding {self.block_reward} ")
            node.reward = self.block_reward
        else:
            print(
                f"Block {block.hash()} rejected. Does not satisfy difficulty {self.difficulty}"
            )


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
        self.transactions = transactions
        self.nonce = nonce

    def __str__(self) -> str:
        result = "Block:\n"
        for i, tx in enumerate(self.transactions):
            result += f"\n\tTransaction {i}:\n\t\t{str(tx)}"
        return result

    def hash(self):
        block_data = str(
            [self.previous_hash, self.timestamp, self.transactions, self.nonce]
        ).encode()
        return sha256(block_data).hexdigest()


class Node:
    def __init__(self, blockchain) -> None:
        self.blockchain = blockchain
        self.reward = 0

    def mine(self, block) -> int:
        hash = block.hash()
        # A valid hash is found when the hash is smaller than the difficulty number
        while hash[: self.blockchain.difficulty] > "0" * self.blockchain.difficulty:
            nonce = random.randint(1, 9999999999999)
            block.nonce = nonce
            hash = block.hash()
        return nonce


class Transaction:
    def __init__(
        self,
        sender,
        recipient,
        amount,
        signature=None,
    ) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def __str__(self) -> str:
        return f"TX: ({self.amount} Blu FROM sender: {self.sender.to_der().hex()} -> recipient: {self.recipient.to_der().hex()})"


class Wallet:
    def __init__(
        self, blockchain=None, node=None, privkey=None, nickname=None, peer_nicknames={}
    ) -> None:
        self.blockchain = blockchain
        self.node = node
        self.privkey = privkey if privkey else SigningKey.generate(curve=SECP256k1)
        self.pubkey = self.privkey.verifying_key
        self.nickname = nickname
        self.peer_nicknames = peer_nicknames

    def send(self, recipient, amount):
        # To send, we need to:
        # 1 - Create a transaction
        # 2 - Sign the transaction
        # 3 - Add to pool of pending transactions
        tx = Transaction(self.pubkey, recipient, amount)
        tx.signature = self.sign(tx)
        self.blockchain.pending_transactions.append(tx)

    def sign(self, transaction):
        # In this case, the "message" is the bytes of our transaction
        return self.privkey.sign(str(transaction).encode())

    def verify(self, signature, transaction):
        return self.pubkey.verify(signature, str(transaction).encode())

    # def get_reward(self):


    def unverified_balance(self):
        # Unverified balance are the unverified transactions in pending_transactions
        unverified_balance = 0
        for tx in self.blockchain.pending_transactions:
            if tx.recipient == self.pubkey:
                unverified_balance += tx.amount
        return unverified_balance

    def verified_balance(self):
        # These are transactions that have been included in the blockchain
        verified_balance = 0
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.recipient == self.pubkey:
                    verified_balance += tx.amount
        return verified_balance

    def balance(self):
        # loop thru blockchain and add up tx's sent to account
        # (assuming no coinbase tx's)
        return self.verified_balance() + self.unverified_balance()

    # TODO: Get txns and associate them with nicknames for ease of use!
    def set_nickname(self, nickname):
        self.nickname = nickname

    def add_peer_nickname(self, verifying_key, peer_nickname):
        # Change ECDSA library type "VerifyingKey" to DER string
        peer_pubkey = self.der(verifying_key)
        self.peer_nicknames[peer_pubkey] = peer_nickname

    # FIXME: no longer using der format, rename
    def der(self, pubkey):
        """
        Convert pubkey to hex string in der format
        """
        return pubkey.to_string().hex()

    def get_mempool_txns(self):
        """
        Show all transactions between for user's wallet in the mempool waiting to be confirmed
        """
        txns = []
        for tx in self.blockchain.pending_transactions:
            if tx.recipient == self.pubkey or tx.sender == self.pubkey:
                txns.append(tx)
        return txns

    def get_confirmed_txns(self):
        """
        Get Txns for user's wallet that have been confirmed and are on the blockchain
        """
        txns = []
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.recipient == self.pubkey or tx.sender == self.pubkey:
                    txns.append(tx)
        return txns

    def get_all_txns(self):
        """
        Get all sent and received Txns for the current wallet
        """
        return self.get_mempool_txns() + self.get_confirmed_txns()

    def show_txns(self, txns):
        """Display txns, mapping peer_nicknames when and user nickname where applicable
        Sample txns output:
            - Bob -> Alice: (10 Blu)
            - Alice -> Chris: (1 Blu)
            - Chris -> Alice: (3 Blu)
        """
        txns_string = ""
        for tx in txns:
            user_pubkey_hex = self.der(self.pubkey)
            sender_hex = self.der(tx.sender)
            recipient_hex = self.der(tx.recipient)

            tx_string = "\t- "
            if tx.sender == self.pubkey:
                tx_string += (
                    f"{self.nickname}" if self.nickname else f"{user_pubkey_hex}"
                )
            elif self.der(tx.sender) in self.peer_nicknames:
                tx_string += f"{self.peer_nicknames[sender_hex]}"
            else:
                tx_string += sender_hex

            tx_string += " -> "

            if tx.recipient == self.pubkey:
                tx_string += (
                    f"{self.nickname}" if self.nickname else f"{user_pubkey_hex}"
                )
            elif recipient_hex in self.peer_nicknames:
                tx_string += f"{self.peer_nicknames[recipient_hex]}"
            else:
                tx_string += recipient_hex

            txns_string += tx_string + f": ({tx.amount} BLU)" + "\n"

        print(txns_string)
