import win32api # 提供了系统级操作的API
import win32con # 包含了WINAPI 定义的各种常量（窗口大小等）
import win32gui # 提供了对窗口的访问和操作功能
import win32ui # 建立在 win32gui 的基础上，提供了更高级的绘图和用户界面元素操作


# 获取屏幕大小尺寸
def get_dimensions():
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    # 窗口位置
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)

def screenshot(name='ss'):
    hdesktop = win32gui.GetDesktopWindow()
    width, height, left, top = get_dimensions()
    
    # 获取设备上下文，这些上下文提供了屏幕截图，图像处理等操作的接口
    desktop_dc = win32gui.GetWindowDC(hdesktop) # 返回Device content对象
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    # 创建一个内存上下文用来存储截图数据
    mem_dc = img_dc.CreateCompatibleDC()
    
    # 逐位将桌面图片复制并保存到内存设备上下文中
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    mem_dc.BitBlt((0,0), (width, height), 
                img_dc, (left, top), win32con.SRCCOPY)
    screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp')
    
    # 后续处理
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())


def run():
    screenshot()
    with open('ss.bmp', 'rb') as f:
        img = f.read()
    return img


if __name__ == '__main__':
    run()   