import tkinter as tk

def get_screen_size():
    """获取当前屏幕分辨率"""
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height

