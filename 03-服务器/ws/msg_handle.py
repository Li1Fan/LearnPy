import json

'''消息体格式
{
  "method": "xxx",
  "type": "xxx",
  "data": {
    "xxx": "xxx"
  }
}'''


class MegHandle:
    def __init__(self):
        pass

    @staticmethod
    def handle_receive(client, server, msg):
        print("client:{} send message:{}".format(client, msg))
        try:
            msg = json.loads(msg)
            # 请求报文数据
            msg_method = msg.get("method")
            msg_type = msg.get("type")
            msg_data = msg.get("data")
            if msg_method == "POST":
                if msg_type == "auth":
                    if not msg_data:
                        method = "REPLY"
                        type = ""
                        data = {"auth_id": "1234567890"}
                        msg_reply = {"method": method, "type": type, "data": data}
                        client.get("handler").send_message(json.dumps(msg_reply))
                else:
                    client.get("handler").send_close()
        except Exception as e:
            print(e)

    @staticmethod
    def handle_open(client, server):
        print("client:{} arrived".format(client))

    @staticmethod
    def handle_close(client, server):
        print("client:{} left".format(client))
