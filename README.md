# Hyper Liquid Point Farming

## Overview

This is a script that is meant to farm "points" on the trading platform HyperLiquid. The exchange is traded on Arbitrum an ethereum layer 2 but uses gasless transactions besides depositing and withdrawing. This logic aims to trade on two separate machines on the same
network and also using different wallets/accounts. The idea is to avoid being sybil detected via matching ips (vpn), machines, adresses, etc. It also implements a small degree of randomization for positions with coin type, size and trade interval to further avoid sybil detection.

### Setup

1. Install the requirements using this command
```sh
pip3 install -r requirements.txt
```
2. It also might be necessary to install the sdk using:
```sh
pip3 install hyperliquid-python-sdk
```
3. Set up your adresses and keys inside utils/clientConfig.py and utils/config.json:
```python
CLIENT_CONFIG = {
    'signing_key': '',
    'wallet_address': '',
    'api_key': '',
    'api_secret': '',
    'env': 'mainnet',
}
```
```json
{
    "comments": "",
    "secret_key": "",
    "account_address": ""
}
```

# Disclaimer

This does not guarantee that hyperliquid won't flag your account as a sybil and prevent you from earning points so use at your own risk.



