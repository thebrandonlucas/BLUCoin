from blucoin import *

blockchain = Blockchain()
brandon_wallet = Wallet()
laura_wallet = Wallet()

brandon_wallet.send(laura_wallet.pubkey, 10, blockchain)
print(laura_wallet.balance(blockchain))

# print(str(blockchain))

