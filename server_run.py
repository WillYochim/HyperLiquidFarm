
import socket
import json
import utils.server_utils as server_utils
from hyperliquid.utils import constants
from exchange import trade


def start_host_script(host, port, exchange):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server started, listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode("utf-8"))
                print(f"Received from client: {message}")

                is_buy = message['is_buy'] != "True"

                trade.make_trade(message['coin'], is_buy, float(message['sz']), exchange, message['sleep'])

                
                response = {"result": "ok"}
                conn.sendall(json.dumps(response).encode("utf-8"))

if __name__ == "__main__":
    address, info, exchange = server_utils.setup(constants.MAINNET_API_URL, skip_ws=True)
    HOST = "0.0.0.0"  
    PORT = 65432      
    start_host_script(HOST, PORT, exchange)