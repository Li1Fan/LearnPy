# -*- coding: utf-8 -*-
"""
__version__ = '1.0'

Created on 2023.04.12
Author frz

Copyright (c) 2023 Star-Net

WebSocket 客户端
"""
import json
import threading
import time

import websocket


class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_open=self.on_open,
                                         on_close=self.on_close)

    # 当收到 WebSocket 消息时调用
    @staticmethod
    def on_message(ws, message):
        print("Received message: %s" % message)
        print(ws)

    # 当 WebSocket 连接建立时调用
    @staticmethod
    def on_open(ws):
        print("WebSocket connection established")
        # 设置客户端自动发送保活心跳包
        ws.keep_running = True

    # 当 WebSocket 连接关闭时调用
    @staticmethod
    def on_close(ws):
        print("WebSocket connection closed")
        print(ws)

    # 启动客户端
    def start(self):
        thread_ws = threading.Thread(target=self.ws.run_forever)
        thread_ws.start()

    # 关闭客户端
    def close(self):
        self.ws.close()

    def send(self, message):
        self.ws.send(message)


def main():
    ws_client = WebSocketClient("ws://localhost:9001/")
    ws_client.start()
    time.sleep(1)
    data = {"method": "POST", "type": "auth", "data": {}}
    ws_client.send(json.dumps(data))
    time.sleep(3)
    ws_client.close()


if __name__ == '__main__':
    main()
