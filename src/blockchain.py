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