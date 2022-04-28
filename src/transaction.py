from ecdsa import SECP256k1, VerifyingKey
from helper import compress


class Transaction:
    def __init__(
        self,
        sender,
        recipient,
        amount,
        signature=None,
    ) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def __str__(self) -> str:
        return f"TX: ({self.amount} Blu FROM sender: {compress(self.sender)} -> recipient: {compress(self.recipient)})"

    def json_serialize(self, coinbase=False):
        signature = self.signature if coinbase else self.signature.to_string().hex()
        return {
            "sender": self.sender.to_string().hex(),
            "recipient": self.recipient.to_string().hex(),
            "amount": self.amount,
            "signature": signature,
        }

    @staticmethod
    def json_deserialize(json_transaction):
        sender, recipient, amount, signature = (
            json_transaction["sender"],
            json_transaction["recipient"],
            json_transaction["amount"],
            json_transaction["signature"],
        )
        return Transaction(sender, recipient, amount, signature)
