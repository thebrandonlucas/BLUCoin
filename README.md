# BLUCoin Blockchain
> What I cannot create, I do not understand
> - Richard Feynman

A minimal custom blockchain implementation to test my knowledge. Theory is great, but practice is better!

Not a real coin!

Special thanks to [Preston Evans](https://prestonevans.net/) for his [blockchain implementation](https://github.com/preston-evans98/blockchain) and for showing me the Bitcoin world in the first place.

And to [Daniel van Flymen](https://dvf.nyc/) for [this article](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46) showing how to use an API for consensus between nodes.

## Quick Start
```
pipenv shell
pipenv install
python src/server.py <port_number>
```

Defaults to port 5000. Run with multiple ports at once to see consensus and transactions in action!

## Features
- Proof-of-work mining
- Wallet to create transactions, using ECDSA signatures
- Consensus using longest valid chain rule
- Flask API to interact with other nodes (locally, for now)

## Doesn't Feature/TODO's
- Difficulty adjustment
- Coin scarcity
- Smart contract language
- Locktimes
- Block size limit

This was just meant as a challenge for me to make sure

## API
`/mine`

Mine a new block, returns new block result

`/chain`

Retrieve blockchain state

`/consensus`

Find longest valid chain among registered peers. Returns local chain if peers aren't longer or are invalid

`/peers/register` 

Method: `POST`

Register a new node in local peer list

Example body:
```
{
  "peers": ["localhost:5005"]
}
```

`/peers/list`

Lists peer nodes. These are the nodes the local chain will perform consensus against

`/wallet/pubkey`

Return the node's associated wallet pubkey and nickname (if applicable)

`/wallet/send`

Method: `POST`

Send BLU to another node's wallet

Example body:
```
{
  "recipient_pubkey": "027b...5024",
  "amount": 20
}
```

`/wallet/balance`

Get the wallet's balance (Unverified + Verified)

`/wallet/unverified_balance`

Get the wallet's balance that's sitting in the mempool

`/wallet/verified_balance`

Get the balance of the wallet that's confirmed on the blockchain

`/mempool`

Get the pending transactions for the specified node
