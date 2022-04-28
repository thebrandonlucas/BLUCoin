from node import Node
from block import Block
from helper import compress


class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        self.pending_transactions = []
        # The number of prepended zeroes to the 256 bit target number
        self.difficulty = 4
        self.block_reward = 50
        self.peers = []

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
        return

    def add_block(self, block, node):
        # Check the block hash for proof of work
        if block.hash()[: self.difficulty] <= "0" * self.difficulty:
            self.chain.append(block)
            self.pending_transactions = []
            print(f"Block {block.hash()} added!")
            print(f"Rewarded {self.block_reward} to {compress(node.pubkey)}")
        else:
            print(
                f"Block {block.hash()} rejected. Does not satisfy difficulty {self.difficulty}"
            )

    # def get_block_height(hash):
    #     """
    #     Gets a block's height by iterating through the blockchain and
    #     returning the index of the block with the matching hash
    #     """

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

    # TODO: serialize/deserialize peers
    def json_deserialize(self, json_chain, json_peers=None):
        self.chain = [Block().json_deserialize(block) for block in json_chain]
        # self.peers = [Node().json_deserialize(peer) for peer in json_peers]
        
