from head import *

from putin import *
from Trans import *
from WhetherFull import *

version="1.3.3"
Date="2024.11.14"

def chose(c):
    if c=='0':
        whether_Full()
        AloneRep()
    elif c=='1':
        whether_Full()
        MultiRep()
    elif c=='9' or c=='8':
        Trans(c)
    else:
        hello()

def hello():
    print("Ciallo～(∠・ω< )⌒★，这里是由AIlian制作的SC2Replay分析工具，欢迎加入sc2萌新吹毛切磋群924040544哟~")
    print("当前版本{}，更新日期{}".format(version,Date))
    print("请根据以下选项输入：")
    print("0:选择rep文件，分析单个rep")
    print("1:选择包含rep的文件夹，批量分析rep")
    print("8:悬浮文字小插件(demo)")
    print("9:选择本软件生成的excel文件，进行流程练习(demo)")
    choice=input()
    chose(choice)

hello()




