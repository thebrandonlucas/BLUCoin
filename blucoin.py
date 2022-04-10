from time import time
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1
import random


class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        self.pending_transactions = []
        # The number of prepended zeroes to the 256 bit target number
        self.difficulty = 4
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
        return self.create_genesis_block()

    def add_block(self, block, node):
        # Check the block hash for proof of work
        if block.hash()[: self.difficulty] <= "0" * self.difficulty:
            self.chain.append(block)
            self.pending_transactions = []
            print(f"Block {block.hash()} added!")
            print(f"Rewarded {self.block_reward} to {node.pubkey.to_string().hex()}")
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


class Node:
    def __init__(self, blockchain, pubkey=None, accounts={}) -> None:
        self.blockchain = blockchain
        # This is the pubkey that will collect block rewards
        self.pubkey = pubkey
        self.accounts = accounts

    def mine(self, message=""):
        """
        Mine a block by finding creating the block, finding a proof-of-work for it,
        and adding it to the chain.

        """
        if not self.pubkey:
            print(
                "MINING ERROR: No pubkey set to collect block reward, please create a wallet first"
            )
            return
        # Create the Genesis block if the chain is empty
        if len(self.blockchain.chain) == 0:
            self.mine_block(
                previous_hash=None,
                message="Chancellor on brink of second bailout for banks",
            )
            return

        # If the chain is not empty, create normal block
        previous_hash = self.blockchain.get_latest_block().hash()
        pending_transactions = self.blockchain.pending_transactions
        self.mine_block(previous_hash, pending_transactions, message)

    def mine_block(self, previous_hash=None, pending_transactions=[], message=""):
        block = Block(
            previous_hash=previous_hash,
            transactions=pending_transactions,
        )
        coinbase_tx = Transaction(
            self.pubkey, self.pubkey, self.blockchain.block_reward, signature=message
        )
        block.transactions["coinbase"] = coinbase_tx
        self.proof_of_work(block)
        self.blockchain.add_block(block, self)

    def proof_of_work(self, block) -> int:
        """
        Mine a block by finding a Proof-of-Work:
            Find a valid proof by hashing a random nonce with the block's data until
            the provided hash is smaller than the target difficulty. In our case, target
            difficulty is simulated by a number of leading zero's to compare to our hash,
            instead of comparing an actual 256 bit hex number.

        :param block: <object> The block to find a valid proof for
        :returns: <int> The nonce that satisfies the proof-of-work (i.e. the "proof")
        """
        hash = block.hash()
        print("Mining...")
        # A valid hash is found when the hash is smaller than the difficulty number
        while hash[: self.blockchain.difficulty] > "0" * self.blockchain.difficulty:
            nonce = random.randint(1, 9999999999999)
            block.nonce = nonce
            hash = block.hash()
        return nonce

    def add_account(self, wallet):
        """
        Add a new wallet to the wallets managed by this node
        """
        if wallet.nickname:
            self.accounts[wallet.nickname] = wallet
        else:
            self.accounts[wallet.pubkey.der()] = wallet

    def set_blockreward_pubkey(self, pubkey):
        self.pubkey = pubkey


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
        self, blockchain, privkey=None, nickname=None, peer_nicknames={}
    ) -> None:
        self.blockchain = blockchain
        self.privkey = privkey if privkey else SigningKey.generate(curve=SECP256k1)
        self.pubkey = self.privkey.verifying_key
        self.nickname = nickname
        self.peer_nicknames = peer_nicknames

    def send(self, recipient, amount):
        # To send, we need to:
        # 1 - Create a transaction
        # 2 - Sign the transaction
        # 3 - Add to pool of pending transactions
        verified_balance = self.verified_balance()
        if verified_balance < amount:
            print(
                f"Transaction failed, {self.nickname} attempted to send {amount} BLU but only had {verified_balance}"
            )
            return

        tx = Transaction(self.pubkey, recipient, amount)
        tx.signature = self.sign(tx)
        self.blockchain.pending_transactions.append(tx)

    def sign(self, transaction):
        # In this case, the "message" is the bytes of our transaction
        return self.privkey.sign(str(transaction).encode())

    def verify(self, signature, transaction):
        return self.pubkey.verify(signature, str(transaction).encode())

    def unverified_balance(self):
        # Unverified balance are the unverified transactions in pending_transactions
        unverified_balance = 0
        for tx in self.blockchain.pending_transactions:
            if tx.recipient == self.pubkey:
                unverified_balance += tx.amount
            elif tx.sender == self.pubkey:
                unverified_balance -= tx.amount
        return unverified_balance

    def verified_balance(self):
        # These are transactions that have been included in the blockchain
        verified_balance = 0
        for block in self.blockchain.chain:
            coinbase_tx = block.transactions["coinbase"]
            if coinbase_tx.recipient == self.pubkey:
                verified_balance += coinbase_tx.amount
            for tx in block.transactions["regular"]:
                if tx.recipient == self.pubkey:
                    verified_balance += tx.amount
                elif tx.sender == self.pubkey:
                    verified_balance -= tx.amount
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
