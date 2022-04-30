import os
from ecdsa import SigningKey
from wallet import Wallet

def write_wallet(privkey, nickname=None) -> str:
    """
    Converts a pubkey to a PEM string for saving to file
    """
    print(os.getcwd())
    if not os.path.isfile("wallet/privkey.pem"):
        with open("wallet/privkey.pem", "wb") as f:
            f.write(privkey.to_pem())
    if nickname and not os.path.isfile("wallet/nickname.db"):
        with open("wallet/nickname.db", "w") as f:
            f.write(nickname)

def read_wallet(blockchain):
    """
    Converts a PEM string to an ECDSA VerifyingKey
    If no privkey file is found, creates a wallet
    """
    # FIXME: Running two different nodes on the same machine
    # loads the same wallet for both of them
    # if os.path.isfile("wallet/privkey.pem"):
    #     with open("wallet/privkey.pem") as f:
    #         privkey = SigningKey.from_pem(f.read())
    #         if os.path.isfile("wallet/nickname.db"):
    #             with open("wallet/nickname.db") as nickname_file:
    #                 nickname = nickname_file.read()
    #                 return Wallet(blockchain, privkey, nickname)
    return Wallet(blockchain)