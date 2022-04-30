from ecdsa import SigningKey, SECP256k1
from transaction import Transaction
from helper import compress


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
        # In this case, the "message" is the bytes of our transaction (minus the empty sig)
        tx_encoded = str(
            {
                "sender": transaction.sender,
                "recipient": transaction.recipient,
                "amount": transaction.amount,
            }
        ).encode()
        return self.privkey.sign(tx_encoded)

    def verify(self, signature, transaction):
        # Since "signature" was empty during tx signing, we don't include it for verifying
        tx_encoded = str(
            {
                "sender": transaction.sender,
                "recipient": transaction.recipient,
                "amount": transaction.amount,
            }
        ).encode()
        return self.pubkey.verify(signature, tx_encoded)

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
        peer_pubkey = self.compress(verifying_key)
        self.peer_nicknames[peer_pubkey] = peer_nickname

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
            user_pubkey_hex = compress(self.pubkey)
            sender_hex = compress(tx.sender)
            recipient_hex = compress(tx.recipient)

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
