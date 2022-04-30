import unittest
import sys, os


# Get relative path to blockchain files
script_dir = os.path.dirname(__file__)
module_dir = os.path.join(script_dir, "..", "src")
sys.path.append(module_dir)

from blockchain import Blockchain
from wallet import Wallet
from node import Node
from block import Block

class TestBlockchain(unittest.TestCase):
    def test_mining_creates_coinbase_tx(self):
        blockchain = Blockchain()

        brandon_node = Node(blockchain)
        brandon_wallet = Wallet(
            blockchain,
            nickname="brandon",
        )
        brandon_node.add_account(brandon_wallet)
        brandon_node.set_blockreward_pubkey(brandon_wallet.pubkey)
        brandon_node.mine()

        coinbase_tx = blockchain.chain[0].transactions["coinbase"]
        self.assertEqual(coinbase_tx.amount, 50)

    def test_miner_receives_reward(self):
        blockchain = Blockchain()

        brandon_node = Node(blockchain)
        brandon_wallet = Wallet(
            blockchain,
            nickname="brandon",
        )
        brandon_node.add_account(brandon_wallet)
        brandon_node.set_blockreward_pubkey(brandon_wallet.pubkey)
        brandon_node.mine()

        # 50 is block reward for mining
        self.assertEqual(brandon_wallet.verified_balance(), 50)

    def test_send_blucoin_pending_tx(self):
        blockchain = Blockchain()

        brandon_node = Node(blockchain)
        laura_wallet = Wallet(blockchain)

        brandon_wallet = Wallet(blockchain, nickname="brandon")
        brandon_node.add_account(brandon_wallet)
        # TODO: set blockreward pubkey by default when adding account
        # set_blockreward_pubkey should just be used to change the pubkey
        brandon_node.set_blockreward_pubkey(brandon_wallet.pubkey)
        brandon_node.mine()

        brandon_wallet.send(laura_wallet.pubkey, 25)

        self.assertEqual(laura_wallet.unverified_balance(), 25)
        self.assertEqual(laura_wallet.balance(), 25)
        self.assertEqual(laura_wallet.verified_balance(), 0)

    def test_send_blucoin_validated_tx(self):
        blockchain = Blockchain()

        brandon_node = Node(blockchain)
        laura_wallet = Wallet(blockchain)

        brandon_wallet = Wallet(blockchain, nickname="brandon")
        brandon_node.add_account(brandon_wallet)
        # TODO: set blockreward pubkey by default when adding account
        # set_blockreward_pubkey should just be used to change the pubkey
        brandon_node.set_blockreward_pubkey(brandon_wallet.pubkey)
        brandon_node.mine()

        brandon_wallet.send(laura_wallet.pubkey, 25)

        # Validate the transaction by mining
        brandon_node.mine()

        self.assertEqual(laura_wallet.unverified_balance(), 0)
        self.assertEqual(laura_wallet.balance(), 25)
        self.assertEqual(laura_wallet.verified_balance(), 25)

    def test_verify_valid_tx(self):
        blockchain = Blockchain()

        brandon_node = Node(blockchain)
        laura_wallet = Wallet(blockchain)

        brandon_wallet = Wallet(blockchain, nickname="brandon")
        brandon_node.add_account(brandon_wallet)
        # TODO: set blockreward pubkey by default when adding account
        # set_blockreward_pubkey should just be used to change the pubkey
        brandon_node.set_blockreward_pubkey(brandon_wallet.pubkey)
        brandon_node.mine()

        brandon_wallet.send(laura_wallet.pubkey, 25)

        brandon_node.mine()

        # Validate the transaction by mining
        tx_to_verify = blockchain.chain[1].transactions["regular"][0]

        self.assertEqual(
            brandon_wallet.verify(tx_to_verify.signature, tx_to_verify), True
        )

    def test_valid_chain(self):
        blockchain = Blockchain()
        node = Node(blockchain)
        wallet = Wallet(blockchain)
        node.add_account(wallet)
        node.set_blockreward_pubkey(wallet.pubkey)

        node.mine()
        node.mine()

        self.assertEqual(blockchain.valid_chain(blockchain.chain), True)

    def test_valid_chain_after_json_serialization(self):
        blockchain = Blockchain()
        node = Node(blockchain)
        wallet = Wallet(blockchain)
        node.add_account(wallet)
        node.set_blockreward_pubkey(wallet.pubkey)

        node.mine()
        node.mine()

        serialized_chain = blockchain.json_serialize()
        deserialized_chain = Blockchain.json_deserialize(serialized_chain)

        self.assertEqual(blockchain.valid_chain(deserialized_chain.chain), True) 

    def test_invalid_chain(self):
        blockchain = Blockchain()
        node = Node(blockchain)
        wallet = Wallet(blockchain)
        node.add_account(wallet)
        node.set_blockreward_pubkey(wallet.pubkey)

        node.mine()

        blockchain.add_block(Block(previous_hash="random bad hash"), node)

        self.assertEqual(blockchain.valid_chain(blockchain.chain), False)

    def test_hash_after_json_deserialize(self):
        # The deserialized chain must be identical to original
        blockchain = Blockchain()
        node = Node(blockchain)
        wallet = Wallet(blockchain)
        node.add_account(wallet)
        node.set_blockreward_pubkey(wallet.pubkey)

        node.mine()

        serialized_chain = blockchain.json_serialize()

        self.assertEqual(
            blockchain.chain[0].hash(),
            Blockchain.json_deserialize(serialized_chain).chain[0].hash(),
        )

if __name__ == "__main__":
    unittest.main()
