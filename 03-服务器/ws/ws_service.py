# -*- coding: utf-8 -*-
"""
__version__ = '1.0'

Created on 2023.04.12
Author frz

Copyright (c) 2023 Star-Net

WebSocket 服务端
自带保活机制，客户端每隔 10 秒发送一次心跳包，如果 30 秒内没有收到心跳包，则断开连接
"""
import threading

from SDUM.src.util.msg_handle import MegHandle
from websocket_server import WebsocketServer


class WsService:
    def __init__(self, port):
        self.port = port
        # 注册回调函数
        self.server = WebsocketServer(port=self.port)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)

    # 当新的 WebSocket 连接建立时调用
    @staticmethod
    def new_client(client, server):
        MegHandle.handle_open(client, server)

    # 当 WebSocket 连接关闭时调用
    @staticmethod
    def client_left(client, server):
        MegHandle.handle_close(client, server)

    # 当收到 WebSocket 消息时调用
    @staticmethod
    def message_received(client, server, message):
        MegHandle.handle_receive(client, server, message)

    # 启动服务器
    def start(self):
        thread_server = threading.Thread(target=self.server.run_forever)
        thread_server.start()

    # 关闭服务器
    def stop(self):
        self.server.shutdown()


if __name__ == '__main__':
    ws_service = WsService(9001)
    ws_service.start()
