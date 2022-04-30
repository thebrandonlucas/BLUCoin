from ecdsa import SECP256k1, VerifyingKey
from helper import compress
import json


class Transaction:
    def __init__(
        self,
        sender,
        recipient,
        amount,
        signature="",
    ) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def __str__(self) -> str:
        return json.dumps(self.json_serialize())

    def json_serialize(self):
        # A coinbase transaction will have a signature of type "str"
        # A regular transaction will have a signature of type "bytes"?
        signature = (
            self.signature
            if isinstance(self.signature, str)
            else self.signature.hex()
        )
        return {
            "sender": self.sender.to_string().hex(),
            "recipient": self.recipient.to_string().hex(),
            "amount": self.amount,
            "signature": signature,
        }

    @staticmethod
    def json_deserialize(json_transaction):
        # TODO: what to do about transaction signatures that are not coinbase? Do we need
        # to do from_string for sigs too?
        sender, recipient, amount, signature = (
            VerifyingKey.from_string(
                bytearray.fromhex(json_transaction["sender"]), curve=SECP256k1
            ),
            VerifyingKey.from_string(
                bytearray.fromhex(json_transaction["recipient"]), curve=SECP256k1
            ),
            json_transaction["amount"],
            json_transaction["signature"],
        )
        return Transaction(sender, recipient, amount, signature)
