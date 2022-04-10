import unittest

from blucoin.src.blockchain import Blockchain
from blucoin.src.node import Node
from blucoin.src.wallet import Wallet


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

    print('brandon wallet BLU: ', brandon_wallet.verified_balance())

    laura_wallet = Wallet(blockchain, nickname="laura")

    brandon_wallet.send(laura_wallet.pubkey, 50)

    print('brandon wallet verified after sending: ', brandon_wallet.verified_balance())
    print('brandon wallet unverified after sending: ', brandon_wallet.unverified_balance())
    print('brandon wallet total after sending ', brandon_wallet.balance())

    print('laura wallet verified after receiving ', laura_wallet.verified_balance())
    print('laura wallet unverified after receiving ', laura_wallet.unverified_balance())
    print('laura wallet total after receiving ', laura_wallet.balance())

    brandon_node.mine()

    print('brandon wallet verified after mining: ', brandon_wallet.verified_balance())
    print('brandon wallet unverified after mining: ', brandon_wallet.unverified_balance())
    print('brandon wallet total after mining ', brandon_wallet.balance())

    print('laura wallet verified after mining ', laura_wallet.verified_balance())
    print('laura wallet unverified after mining ', laura_wallet.unverified_balance())
    print('laura wallet total after mining ', laura_wallet.balance())
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
    def test_node(self):
        blockchain = generate_transactions()
        # print(blockchain)

    # def test_init(self):
    #     blockchain = Blockchain()
    #     self.assertEqual(blockchain.chain, [])
    #     self.assertEqual(blockchain.pending_transactions, [])

    # def test_add_block(self):
    #     blockchain = generate_transactions()

    #     block = Block(
    #         previous_hash=blockchain.get_latest_block().hash(),
    #         transactions=blockchain.pending_transactions,
    #     )
    #     node = Node(blockchain)
    #     # miner_wallet = Wallet(blockchain=blockchain, node=node)
    #     node.mine(block)
    #     blockchain.add_block(block, node)

    #     self.assertEqual(len(blockchain.chain), 1)
    #     self.assertEqual(blockchain.pending_transactions, [])
    #     self.assertEqual(blockchain.chain[0].hash(), block.hash())
    #     self.assertEqual(node.reward, 50)


# class TestBlock(unittest.TestCase):
#     # def test_hash(self):
#     #     blockchain = Blockchain()
#     #     blockchain.add_block()
#     #     blockchain.add_block()

#     #     previous_hash_last_block = blockchain.get_latest_block().previous_hash
#     #     hash_of_first_block = blockchain.chain[0].hash()
#     #     self.assertEqual(previous_hash_last_block, hash_of_first_block)
#     # def test_hash(self):
#     # block = Block()
#     pass


# class TestNode(unittest.TestCase):
#     def test_mine(self):
#         blockchain = Blockchain()
#         brandon_wallet = Wallet(blockchain)
#         laura_wallet = Wallet(blockchain)
#         tom_wallet = Wallet(blockchain)

#         brandon_wallet.set_nickname("Brandon")
#         brandon_wallet.add_peer_nickname(laura_wallet.pubkey, "Laura")
#         brandon_wallet.add_peer_nickname(tom_wallet.pubkey, "Tom")

#         brandon_wallet.send(laura_wallet.pubkey, 123)
#         laura_wallet.send(brandon_wallet.pubkey, 33)
#         brandon_wallet.send(tom_wallet.pubkey, 12)
#         tom_wallet.send(brandon_wallet.pubkey, 24)

#         block = Block(transactions=blockchain.pending_transactions)

#         node = Node(blockchain)
#         proof = node.mine(block)

#         # Test that the proof correctly hashes
#         block_data = str(
#             [block.previous_hash, block.timestamp, block.transactions, proof]
#         ).encode()
#         self.assertEqual(sha256(block_data).hexdigest(), block.hash())

#         # Test that the hash is below the difficulty
#         self.assertLessEqual(
#             block.hash()[: blockchain.difficulty], "0" * blockchain.difficulty
#         )


# class TestWallet(unittest.TestCase):
#     def test_send(self):
#         blockchain = Blockchain()
#         my_wallet = Wallet(blockchain)
#         peer_wallet = Wallet(blockchain)
#         my_wallet.send(peer_wallet.pubkey, 10)

#         self.assertEqual(peer_wallet.balance(), 10)

#     def test_verify(self):
#         blockchain = Blockchain()
#         my_wallet = Wallet(blockchain)
#         peer_wallet = Wallet(blockchain)
#         my_wallet.send(peer_wallet.pubkey, 10)
#         tx = blockchain.pending_transactions[0]

#         self.assertEqual(my_wallet.verify(tx.signature, tx), True)

#     def test_unverified_balance_empty(self):
#         blockchain = Blockchain()
#         my_wallet = Wallet(blockchain)
#         self.assertEqual(my_wallet.unverified_balance(), 0)

#     def test_unverified_balance_not_empty(self):
#         blockchain = Blockchain()
#         my_wallet = Wallet(blockchain)
#         peer_wallet = Wallet(blockchain)
#         my_wallet.send(peer_wallet.pubkey, 10)

#         self.assertEqual(peer_wallet.unverified_balance(), 10)

#     def test_add_peer_nickname(self):
#         my_wallet = Wallet()
#         peer_wallet = Wallet()
#         my_wallet.add_peer_nickname(peer_wallet.pubkey, "Laura")

#         peer_pubkey_der = peer_wallet.pubkey.to_string().hex()
#         self.assertEqual(my_wallet.peer_nicknames[peer_pubkey_der], "Laura")

#     def test_show_txns(self):
#         blockchain = Blockchain()
#         brandon_wallet = Wallet(blockchain)
#         laura_wallet = Wallet(blockchain)
#         tom_wallet = Wallet(blockchain)

#         brandon_wallet.set_nickname("Brandon")
#         brandon_wallet.add_peer_nickname(laura_wallet.pubkey, "Laura")
#         brandon_wallet.add_peer_nickname(tom_wallet.pubkey, "Tom")

#         brandon_wallet.send(laura_wallet.pubkey, 123)
#         laura_wallet.send(brandon_wallet.pubkey, 33)
#         brandon_wallet.send(tom_wallet.pubkey, 12)
#         tom_wallet.send(brandon_wallet.pubkey, 24)

#         txns = brandon_wallet.get_all_txns()
#         brandon_wallet.show_txns(txns)


if __name__ == "__main__":
    unittest.main()
