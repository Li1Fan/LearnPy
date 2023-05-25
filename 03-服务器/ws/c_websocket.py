# -*- coding: utf-8 -*-
"""
Created on 2022.10.9
Author frz

WebSocket客户端
"""
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed

IP_ADDR = "127.0.0.1"
IP_PORT = "8888"


# 握手，通过发送hello，接收success来进行双方的握手。
async def clientHands(websocket):
    # while True:
    try:
        await websocket.send("hello")
        response_str = await websocket.recv()
        if "success" in response_str:
            print("握手成功")
            return True
    except Exception as e:
        print(e)


# 向服务器端发送消息
async def clientSend(websocket):
    try:
        while True:
            input_text = input("input text: ")
            if input_text == "exit":
                print(f'"exit", bye!')
                await websocket.close(reason="exit")
                return False
            await websocket.send(input_text)
            recv_text = await websocket.recv()
            print(f"{recv_text}")
    except ConnectionClosed as e:
        print(e.code)
        if e.code == 1006:
            print('server close')


# 进行websocket连接
async def clientRun():
    ipaddress = IP_ADDR + ":" + IP_PORT
    async with websockets.connect("ws://" + ipaddress) as websocket:
        if await clientHands(websocket):
            await clientSend(websocket)


# 客户端主函数
def client_main():
    print("======client main begin======")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(clientRun())


if __name__ == "__main__":
    client_main()
