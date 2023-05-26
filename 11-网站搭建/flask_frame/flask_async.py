import asyncio
from flask import Flask

app = Flask(__name__)


@app.route('/')
async def hello():
    await asyncio.sleep(1)  # 模拟耗时操作
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
