import socket
import json
import time
import random
import utils.client_utils as client_utils
from hyperliquid.utils import constants



def start_client(host, port):


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        while True:
            trade = client_utils.generate_trade_data()

            s.sendall(json.dumps(trade).encode("utf-8"))
            
            data = s.recv(1024)
            parsed = json.loads(data.decode('utf-8'))
            if(parsed['result'] == 'ok'):
                print("Making Trade")
                client_utils.make_trade(trade['coin'], eval(trade['is_buy']), float(trade['sz']), trade['sleep'])


HOST = "192.168.2.15"
PORT = 65432
address, info, exchange = client_utils.setup(constants.MAINNET_API_URL, skip_ws=True)
start_client(HOST, PORT)
