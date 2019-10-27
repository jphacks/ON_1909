import time
import math
from websocket_server import WebsocketServer
from websocket import create_connection

def main():
    ws = create_connection("wss://9ws.obniz.io/obniz/7479-8965/ws/1")

    for i in range(6):
        content =  ws.recv()
        result = content[47:-3]
        result = result.strip("[")
        result = result.strip("]")
        result = result.split(',')

        if(len(result) == 3):
            first_data = int(result[1])
            print("{}".format(first_data))

    print("-----------")

    while True:
        content =  ws.recv()
        result = content[47:-3]
        result = result.strip("[")
        result = result.strip("]")
        result = result.split(',')

        if (len(result) == 3):

            data = int(result[1])

            if (abs(first_data - data)):
                print("mmomomo")
                print("{}".format(data))
        print("-----------")

    ws.close()

main()
