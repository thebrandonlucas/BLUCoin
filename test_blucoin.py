from blucoin import *

blockchain = Blockchain()
brandon_wallet = Wallet()
laura_wallet = Wallet()

brandon_wallet.send(laura_wallet.pubkey, 10, blockchain)
print(laura_wallet.balance(blockchain))

# print(laura_wallet.verify(blockchain.pending_transactions[0].signature, str(blockchain.pending_transactions[0]).encode()))
# print(blockchain.pending_transactions[0])
# print(str(blockchain))
for tx in blockchain.pending_transactions:
    print(tx)