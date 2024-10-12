import websocket
import json

# 设置一个计数器，用于追踪接收到的消息次数
message_count = 0


# 接收消息的回调函数
def on_message(ws, message):
    global message_count

    print(f"收到消息: {message}")

    # 计数器递增
    message_count += 1

    if message_count == 1:
        # 第一次收到消息时发送第一条消息内容
        data_to_send = {
            "userName": "98e999e4d2",
            "event": "REGISTER"
        }
        # 将字典转为JSON字符串
        message_to_send = json.dumps(data_to_send)
        # 发送消息给服务器
        ws.send(message_to_send)
        print(f"发送消息到服务器: {message_to_send}")

    elif message_count == 2:
        # 第二次收到消息时发送第二条消息内容
        data_to_send = {
            "event": "LIST_MAIL"
        }
        # 将字典转为JSON字符串
        message_to_send = json.dumps(data_to_send)
        # 发送消息给服务器
        ws.send(message_to_send)
        print(f"发送消息到服务器: {message_to_send}")


def on_error(ws, error):
    print(f"错误: {error}")


def on_close(ws, close_status_code, close_msg):
    print("连接关闭")


def on_open(ws):
    print("WebSocket 连接已打开")


# 构建 WebSocket 连接
def create_websocket_connection():
    websocket_url = "wss://mail.ipwangxin.cn/ws/email"

    headers = {
        "Origin": "https://mail.ipwangxin.cn",
        "Cache-Control": "no-cache",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Sec-WebSocket-Key": "TFScdBexdmv+/Eef2aLhPA==",
        "Sec-WebSocket-Version": "13"
    }

    # 初始化 WebSocket 连接
    ws = websocket.WebSocketApp(
        websocket_url,
        header=headers,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # 开启 WebSocket 连接
    ws.run_forever()


# 调用 WebSocket 连接
if __name__ == "__main__":
    create_websocket_connection()
