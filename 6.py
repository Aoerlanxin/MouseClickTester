import sys
import ctypes
import time
from pathlib import Path


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # 重新以管理员权限运行脚本
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

# ===== 以下是你的主程序 =====
import pyautogui
from pynput import mouse

# 获取桌面路径并创建输出文件
desktop_path = Path.home() / "Desktop"
output_file = desktop_path / "mouse_clicks.txt"

# 确保文件存在，如果不存在则创建
if not output_file.exists():
    output_file.touch()

time.sleep(5)

def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            click_info = f"{x},{y}"
            print(click_info)  # 同时在控制台输出
            # 写入到文件
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(click_info + '\n')
        elif button == mouse.Button.right:
            stop_info = "检测到右键点击，停止监听"
            print(stop_info)
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(stop_info + '\n')

            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(start_info + '\n')
            return False

start_info = "开始监听鼠标点击位置（左键输出坐标，右键停止）..."
print(start_info)

with mouse.Listener(on_click=on_click) as listener:
    listener.join()

end_info = "程序已停止"
print(end_info)
with open(output_file, 'a', encoding='utf-8') as f:
    f.write(end_info + '\n')