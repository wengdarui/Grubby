import websocket
import logging
import json
import asyncio
import _thread as thread
import websocket
import websockets
import time
from websocket import create_connection

# ws = create_connection("ws://172.16.3.11:9090/ws")
# print("+++++++++")
# data={}
# data['clientId'] = 'client123'
# data['topic'] = 'DH/test/#'
# data['deviceId'] = ["tiger_dream_007"]
# data=json.dumps(data)
# ws.send(data)
# print("+++++++++")
# result = ws.recv()
# print(result)


# url = 'ws://172.16.3.11:9090/ws'
# while True:  # 一直链接，直到连接上就退出循环
#     time.sleep(2)
#     try:
#         ws = create_connection(url)
#         print(ws)
#         break
#     except Exception as e:
#         print('连接异常：', e)
#         continue
# while True:  # 连接上，退出第一个循环之后，此循环用于一直获取数据
#     data={}
#     data['clientId'] = 'client123'
#     data['topic'] = 'DH/test/#'
#     data['deviceId'] = ["tiger_dream_007"]
#     data=json.dumps(data)
#     ws.send(data)
#     response = ws.recv()
#     print(response)
#

import json
from ws4py.client.threadedclient import WebSocketClient


class CG_Client(WebSocketClient):

    def opened(self):
        req = '{"clientId": "client1234", "topic": "DH/test/#", "deviceId": ["tiger_dream_0","tiger_dream_1","tiger_dream_2","tiger_dream_3","tiger_dream_4"]}'
        self.send(req)

    def closed(self, code, reason=None):
        print("Closed down:", code, reason)

    def received_message(self, resp):
        resp = json.loads(str(resp))
        print(resp)
        # data = resp['data']
        # if type(data) is dict:
        #     ask = data['asks'][0]
        #     print('Ask:', ask)
        #     bid = data['bids'][0]
        #     print('Bid:', bid)


if __name__ == '__main__':
    ws = None
    try:
        # ws = CG_Client('ws://172.16.3.11:9090/ws')
        ws = CG_Client('ws://192.168.10.115:3306//chat/ws')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()