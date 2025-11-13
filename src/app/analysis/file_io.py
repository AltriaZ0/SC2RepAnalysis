from tkinter import *
from tkinter import filedialog, messagebox
from pathlib import Path
import os
import sys
import logging

LOG = logging.getLogger("app.file_io")

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

def get_replay_dir():
    # print("下面，选择想要分析的reps所在的文件夹吧~")
    R = Tk()
    R.withdraw() 
    R.title("选择replay文件夹")
    dir=filedialog.askdirectory()
    R.withdraw()

    if not dir:
        messagebox.showerror(title='QAQ ~', message="没有选择文件夹哦~")
        sys.exit()

    # 统计文件数量
    filesnum=0
    for r,d,f in os.walk(dir):
        for file in f:
            if file[-9:]=="SC2Replay":
                filesnum+=1

    if filesnum==0:
        messagebox.showerror(title='QAQ ~', message="选择的文件夹里没有replay文件呀~")
        sys.exit()

    LOG.info("选取的录像文件夹所在的路径是{},伦家会在这里创建Rep分析文件夹哦~".format(dir))
    LOG.info("当前文件夹中一共有{}个rep文件，开始解析......".format(filesnum))

    return dir