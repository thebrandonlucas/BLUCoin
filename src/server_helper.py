import sys

def get_port():
    """
    Gets the port number to use (for multiple nodes running on the same machine)
    Defaults to 5000, but user can bypass using system commands
    """
    if len(sys.argv) > 1:
        port = sys.argv[1]
        return port
    return 5000

def compress(pubkey):
    """
    Convert pubkey to hex string in compressed format
    Read more: https://github.com/tlsfuzzer/python-ecdsa
    """
    return pubkey.to_string("compressed").hex()



