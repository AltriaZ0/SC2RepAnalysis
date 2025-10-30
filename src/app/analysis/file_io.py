from tkinter import *
from tkinter import filedialog, messagebox
from pathlib import Path


def get_replay_path():
    """
    弹出文件选择对话框，返回选择的文件路径
    """
    R = Tk()
    R.withdraw() 
    R.title("选择replay文件")
    p=filedialog.askopenfilename()
    path = Path(p)
    return path
