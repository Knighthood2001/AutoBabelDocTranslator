from getScreenSize import get_screen_size

try:
    width, height = get_screen_size()
    print(f"屏幕分辨率：{width}x{height}")
except Exception as e:
    print(f"获取失败：{e}")


