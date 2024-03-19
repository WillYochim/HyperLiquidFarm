
import time
def make_trade(coin, is_buy, sz, exchange, sleep):

    print(f"Market {'Buy' if is_buy else 'Sell'} {sz} {coin}.")

    order_result = exchange.market_open(coin, is_buy, sz, None, 0.01)
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