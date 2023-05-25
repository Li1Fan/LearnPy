# -*- coding: utf-8 -*-
"""
Created on 2022.10.9
Author frz

WebSocket服务端
"""
import asyncio
import threading
import websockets
from websockets.exceptions import ConnectionClosed

IP = "127.0.0.1"
PORT = "8888"


# 握手，通过接收hello，发送success来建立双方的握手
async def serverHands(websocket):
    try:
        recv_text = await websocket.recv()
        print("recv_text=" + recv_text)
        if recv_text == "hello":
            print("success!")
            await websocket.send("connect success")
            return True
        else:
            await websocket.send("connect fail")
            await websocket.close()
            return False
    except ConnectionClosed as e:
        if e.code == 1000:
            print('client close')


# 接收从客户端发来的消息并处理，再返给客户端ok
async def serverRecv(websocket):
    try:
        while True:
            # 这里忽略处理，直接打印消息
            recv_text = await websocket.recv()
            print("recv:", recv_text)
            await websocket.send("ok!!!")
    except ConnectionClosed as e:
        print(e.code)
        if e.code == 1000:
            print('client close')


# 握手并且接收数据，这里可以存储websocket对象
async def serverRun(websocket, path):
    if await serverHands(websocket):
        await serverRecv(websocket)


# 服务端主函数
def server_main():
    print("======server main begin======")
    server = websockets.serve(serverRun, IP, PORT, ping_interval=None)  # ping_interval设置为None，取消超时关闭
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server)
    loop.run_forever()


class AsyThread(threading.Thread):
    """协程与线程结合"""

    def __init__(self, loop):
        threading.Thread.__init__(self)
        self.mLoop = loop

    def run(self):
        asyncio.set_event_loop(self.mLoop)  # 在新线程中开启一个事件循环
        self.mLoop.run_until_complete(server_main())


if __name__ == "__main__":
    server_main()
    # 以线程执行主函数
    # newLoop = asyncio.new_event_loop()
    # t = AsyThread(newLoop)
    # t.start()