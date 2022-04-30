from blockchain.node import Node
from blockchain.block import Block
from server.server_helper import compress
import requests
import json


class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        self.pending_transactions = []
        # The number of prepended zeroes to the 256 bit target number
        self.difficulty = 4
        self.block_reward = 50
        self.peers = set()

    def __str__(self):
        return json.dumps(self.json_serialize())

    def get_latest_block(self):
        if len(self.chain):
            return self.chain[-1]
        return

    def add_block(self, block, node):
        # Check the block hash for proof of work
        if block.hash()[: self.difficulty] >= "0" * self.difficulty:
            self.chain.append(block)
            self.pending_transactions = []
            print(f"Block {block.hash()} added!")
            print(f"Rewarded {self.block_reward} to {compress(node.pubkey)}")
        else:
            print(
                f"Block {block.hash()} rejected. Does not satisfy difficulty {self.difficulty}"
            )

    def register_peers(self, peers):
        """
        Register a neighboring node to compare their blockchains
        """
        # Convert to set() from list so we don't add duplicate peers
        for peer in peers:
            self.peers.add(peer)

    def valid_chain(self, chain):
        """
        Determines whether the given chain is valid by checking:
            1) If the hash of a block is the previous hash of the next block (i.e. are they linked?)
            2) If the proof used in each block is a valid difficulty
        """
        prev_block = None
        for block in chain:

            # Check if current block is Genesis
            if block.previous_hash == None:
                # Can't have two Genesis blocks!
                if prev_block:
                    return False
                prev_block = block
                continue
            
            if block.previous_hash != prev_block.hash():
                return False
            if not block.valid_proof(self.difficulty):
                return False

            prev_block = block
        return True

    def consensus(self):
        """
        The consensus algorithm that compares our chain to our neighbors and gets
        the one with the longest valid proof-of-work

        Returns True if new chain added,
        else False
        """
        current_chain = self.chain
        for node in self.peers:
            # Request the neighbor's blockchain
            response = requests.get(f"http://{node}/chain")
            if response.status_code == 200:
                neighbor_chain = Blockchain.json_deserialize(response.json()).chain
                if self.valid_chain(neighbor_chain) and len(neighbor_chain) > len(
                    current_chain
                ):
                    current_chain = neighbor_chain

        # Return True if new chain added
        if self.chain != current_chain:
            self.chain = current_chain
            return True
        return False

    def json_serialize(self):
        chain = [block.json_serialize() for block in self.chain]
        pending_transactions = [tx.json_serialize() for tx in self.pending_transactions]
        return {
            "chain": chain,
            "pending_transactions": pending_transactions,
            "difficulty": self.difficulty,
            "block_reward": self.block_reward,
            "peers": self.peers,
        }

    @staticmethod
    def json_deserialize(json_blockchain, json_peers=None):
        blockchain = Blockchain()
        blockchain.chain = [Block.json_deserialize(block) for block in json_blockchain["chain"]]
        blockchain.peers = set(json_blockchain["peers"])
        return blockchain
