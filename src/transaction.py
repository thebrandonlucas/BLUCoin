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
        return f"TX: ({self.amount} Blu FROM sender: {self.sender.to_der().hex()} -> recipient: {self.recipient.to_der().hex()})"
