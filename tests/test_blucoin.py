import unittest
import sys, os



# Get relative path to blockchain files
script_dir = os.path.dirname(__file__)
module_dir = os.path.join(script_dir, "..", "src")
sys.path.append(module_dir)

from blockchain import Blockchain
from wallet import Wallet
from node import Node


def generate_transactions():
    blockchain = Blockchain()

    brandon_node = Node(blockchain)
    brandon_wallet = Wallet(
        blockchain,
        nickname="brandon",
    )
    brandon_node.add_account(brandon_wallet)
    brandon_node.set_blockreward_pubkey(brandon_wallet.pubkey)
    brandon_node.mine()

    print("brandon wallet BLU: ", brandon_wallet.verified_balance())

    laura_wallet = Wallet(blockchain, nickname="laura")

    brandon_wallet.send(laura_wallet.pubkey, 50)

    print("brandon wallet verified after sending: ", brandon_wallet.verified_balance())
    print(
        "brandon wallet unverified after sending: ", brandon_wallet.unverified_balance()
    )
    print("brandon wallet total after sending ", brandon_wallet.balance())

    print("laura wallet verified after receiving ", laura_wallet.verified_balance())
    print("laura wallet unverified after receiving ", laura_wallet.unverified_balance())
    print("laura wallet total after receiving ", laura_wallet.balance())

    brandon_node.mine()

    print("brandon wallet verified after mining: ", brandon_wallet.verified_balance())
    print(
        "brandon wallet unverified after mining: ", brandon_wallet.unverified_balance()
    )
    print("brandon wallet total after mining ", brandon_wallet.balance())

    print("laura wallet verified after mining ", laura_wallet.verified_balance())
    print("laura wallet unverified after mining ", laura_wallet.unverified_balance())
    print("laura wallet total after mining ", laura_wallet.balance())
    # print('brandon wallet verified after mining')

    # brandon_wallet = Wallet(blockchain)
    # laura_wallet = Wallet(blockchain)
    # tom_wallet = Wallet(blockchain)

    # brandon_wallet.set_nickname("Brandon")
    # brandon_wallet.add_peer_nickname(laura_wallet.pubkey, "Laura")
    # brandon_wallet.add_peer_nickname(tom_wallet.pubkey, "Tom")

    # brandon_wallet.send(laura_wallet.pubkey, 123)
    # laura_wallet.send(brandon_wallet.pubkey, 33)
    # brandon_wallet.send(tom_wallet.pubkey, 12)
    # tom_wallet.send(brandon_wallet.pubkey, 24)

    return blockchain
    

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

        coinbase_tx = blockchain.chain[0].transactions['coinbase']
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


if __name__ == "__main__":
    unittest.main()
