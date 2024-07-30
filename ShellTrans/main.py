import socket
import threading
import argparse
import logging

from pynput import keyboard

# 是否继续运行
Running = True

def on_press(key):
    global Running
    try:
        # 检查是否按下了 Ctrl+C 组合键
        if key.char == "c" and key.ctrl:
            print("Ctrl+C detected. Exiting...")
            running = False
    except AttributeError:
        pass


def handle_client(local_socket, client_host, client_port):
    try:
        # 连接到远程主机
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((client_host, client_port))

        # 在两个socket之间转发流量
        while Running:
            # 从客户端读取数据
            local_buffer = local_socket.recv(4096)
            if len(local_buffer):
                print(f"[==>] Received {len(local_buffer)} bytes from remote.")
                client_socket.send(local_buffer)
                print(f"[==>] Sent to remote.")

            # 从远程主机读取数据
            client_buffer = client_socket.recv(4096)
            if len(client_buffer):
                print(f"[<==] Received {len(client_buffer)} bytes from client.")
                local_socket.send(client_buffer)
                print(f"[<==] Sent to localhost.")

    except Exception as e:
        print(f"Error: {e}")
        local_socket.close()
        client_socket.close()


def start_server(local_port, client_host, client_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", local_port))
    server.listen(5)
    print(f"[*] Listening on 0.0.0.0:{local_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # 创建一个线程来处理新的客户端连接
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, client_host, client_port)
        )
        client_handler.start()


if __name__ == "__main__":
    # arg paser
    parser = argparse.ArgumentParser(
        prog="TCP Port Forwarder", 
        description="@Author: Ly4hm",
        epilog="Press <Ctrl>+c to quit after current connection complete"
    )
    parser.add_argument(
        "-lp", "--local_port", type=int, required=True, help="Local port to listen on"
    )
    parser.add_argument(
        "-ch", "--client_host", required=True, help="Client host to forward traffic to"
    )
    parser.add_argument(
        "-cp",
        "--client_port",
        type=int,
        required=True,
        help="Client port to forward traffic to",
    )
    args = parser.parse_args()

    # 设置键盘监听器
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    start_server(args.local_port, args.client_host, args.client_port)
    
    listener.stop()
