import eth_account
from eth_account.signers.local import LocalAccount
import json
import os

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
import requests
import datetime
import random
import time


def generate_trade_data():
    COIN_LIST = ["BTC", "ETH"]
    BUY_OR_SELL= ["False", "True"]
    TRADE_DOLLAR_VALUE = [75,90,120,150]
    coin = random.choice(COIN_LIST)
    amount = round(random.choice(TRADE_DOLLAR_VALUE)/ get_price(coin), 4) 
    sleep = random.randint(30,60)
    return {"coin": coin, "is_buy": random.choice(BUY_OR_SELL), "sz": str(amount), "sleep": str(sleep)}



def get_current_time_millis():
    return int(datetime.datetime.now().timestamp() * 1000)

def setup(base_url=None, skip_ws=False):
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path) as f:
        config = json.load(f)
    account: LocalAccount = eth_account.Account.from_key(config["secret_key"])
    address = config["account_address"]
    if address == "":
        address = account.address
    print("Running with account address:", address)
    if address != account.address:
        print("Running with agent address:", account.address)
    info = Info(base_url, skip_ws)
    user_state = info.user_state(address)
    margin_summary = user_state["marginSummary"]
    if float(margin_summary["accountValue"]) == 0:
        print("Not running the example because the provided account has no equity.")
        url = info.base_url.split(".", 1)[1]
        print(f"If you think this is a mistake, make sure that {address} has a balance on {url}.")
        print("If address shown is your API wallet address, update the config to specify account_address")
        raise Exception("No accountValue")
    exchange = Exchange(account, base_url, account_address=address)
    return address, info, exchange

def make_trade(coin, is_buy, sz, exchange, sleep):

    print(f"Market {'Buy' if is_buy else 'Sell'} {sz} {coin}.")

    order_result = exchange.market_open("BTC", is_buy, sz, None, 0.01)
    if order_result["status"] == "ok":
        for status in order_result["response"]["data"]["statuses"]:
            try:
                filled = status["filled"]
                print(f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}')
            except KeyError:
                print(f'Error: {status["error"]}')

        time.sleep(int(sleep))

        print(f"Market Closing: {coin}.")
        order_result = exchange.market_close(coin)
        if order_result["status"] == "ok":
            for status in order_result["response"]["data"]["statuses"]:
                try:
                    filled = status["filled"]
                    print(f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}')
                except KeyError:
                    print(f'Error: {status["error"]}')

def get_price(coin):
    url = "https://api.hyperliquid.xyz/info"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "type": "candleSnapshot",
        "req": {
            "coin": coin,
            "interval": "1m",
            "startTime": get_current_time_millis(),
            "endTime": get_current_time_millis()
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        data = response.json()
        return float(data[0]['c'])
    else:
        return f"Failed to retrieve data, status code: {response.status_code}"
    
