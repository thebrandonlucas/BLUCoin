import random
from blockchain.block import Block
from blockchain.transaction import Transaction
from server.server_helper import compress


class Node:
    def __init__(self, blockchain, pubkey=None, accounts={}) -> None:
        self.blockchain = blockchain
        # This is the pubkey that will collect block rewards
        self.pubkey = pubkey
        self.accounts = accounts

    def mine(self, message=""):
        """
        Mine a block by creating the block, finding a proof-of-work for it,
        and adding it to the chain.
        :returns: <object> block
        """
        if not self.pubkey:
            print(
                "MINING ERROR: No pubkey set to collect block reward, please create a wallet first"
            )
            return
        # Create the Genesis block if the chain is empty
        if len(self.blockchain.chain) == 0:
            return self.mine_block(
                previous_hash=None,
                message="Chancellor on brink of second bailout for banks",
            )

        # If the chain is not empty, create normal block
        previous_hash = self.blockchain.get_latest_block().hash()
        pending_transactions = self.blockchain.pending_transactions
        return self.mine_block(previous_hash, pending_transactions, message)

    def mine_block(self, previous_hash=None, pending_transactions=[], message=""):
        coinbase_tx = Transaction(
            self.pubkey, self.pubkey, self.blockchain.block_reward, signature=message
        )
        block = Block(
            previous_hash=previous_hash,
            transactions={"coinbase": coinbase_tx, "regular": pending_transactions},
        )
        self.proof_of_work(block)
        self.blockchain.add_block(block, self)
        return block

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
            self.accounts[compress(wallet.pubkey)] = wallet

    def set_blockreward_pubkey(self, pubkey):
        self.pubkey = pubkey
