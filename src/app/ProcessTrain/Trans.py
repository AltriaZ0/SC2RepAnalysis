from libs import *
from tkinter import *
from tkinter import filedialog
import pandas as pd
import time
import win32console
import win32gui

#==============================================================SC2ARepnalysis 1.3.0更新内容：流程练习==================================================================#
def Trans(c):
    def refreshText():
        global i,j,b_i
        i=time.time()-k
        i=int(i)
        t="{}:{}".format(i//60,i%60)
        canvas.delete('all')
        if t==seq[j][0]:
            canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(),fill=TRANSCOLOUR, outline=TRANSCOLOUR)
            if j-3>=0:
                canvas.create_text(0,10,text ="{}|{}".format(seq[j-3][0],seq[j-3][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))

            if j-2>=0:
                canvas.create_text(0,35,text ="{}|{}".format(seq[j-2][0],seq[j-2][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))

            if j-1>=0:
                canvas.create_text(0,60,text ="{}|{}".format(seq[j-1][0],seq[j-1][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))
            
            canvas.create_text(0,85,text ="{}|{}".format(seq[j][0],seq[j][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',22,'bold'))


            if j+1<len(seq)-1:
                canvas.create_text(0,115,text ="{}|{}".format(seq[j+1][0],seq[j+1][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))
            if j+2<len(seq)-1:
                canvas.create_text(0,140,text ="{}|{}".format(seq[j+2][0],seq[j+2][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))    
            if j+3<len(seq)-1:
                canvas.create_text(0,165,text ="{}|{}".format(seq[j+3][0],seq[j+3][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))    

            canvas.create_text(0,185,text ="■",fill ='#66CCFF',anchor = W,font =('微软雅黑',20))



            j+=1

        else:        
            canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(),fill=TRANSCOLOUR, outline=TRANSCOLOUR)
            if j-3>=0:
                canvas.create_text(0,10,text ="{}|{}".format(seq[j-3][0],seq[j-3][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))
            if j-2>=0:
                canvas.create_text(0,35,text ="{}|{}".format(seq[j-2][0],seq[j-2][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))
            if j-1>=0:
                canvas.create_text(0,60,text ="{}|{}".format(seq[j-1][0],seq[j-1][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))
            
            canvas.create_text(0,85,text = "{}".format(t),fill ='#66CCFF',anchor = W,font =('微软雅黑',22))
            
            if j+1<len(seq)-1:
                canvas.create_text(0,115,text ="{}|{}".format(seq[j][0],seq[j][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))
            if j+2<len(seq)-1:
                canvas.create_text(0,140,text ="{}|{}".format(seq[j+1][0],seq[j+1][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18)) 
            if j+3<len(seq)-1:
                canvas.create_text(0,165,text ="{}|{}".format(seq[j+2][0],seq[j+2][1]),fill ='#66CCFF',anchor = W,font =('微软雅黑',18))

            canvas.create_text(0,185,text ="■",fill ='#66CCFF',anchor = W,font =('微软雅黑',20))
        if i==0:
            b_i=0
        if b_i!=i:
            canvas.update()
        b_i=i

    def withoutcontrol(self):
        tk.overrideredirect(1) #去除标题栏)

    def draw0(event):
        global relateX,relateY
        relateX=event.x
        relateY=event.y
    def draw(event):
        new_x = tk.winfo_x()-relateX+(event.x)
        new_y = tk.winfo_y()-relateY+event.y
        s = "800x600+{}+{}".format(new_x,new_y)
        tk.geometry(s)

    def back(self):
        print("从头开始！")
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(),fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        canvas.create_text(0,100,text ="将于3秒后开始\n使用说明：\n[1]按住【Ctrl】点击文字可以移动位置\n[2]按【BackSpace】可以重置计时器\n[3]按【ESC】关闭",fill ='#66CCFF',anchor = W,font =('微软雅黑',20))
        canvas.update()
        time.sleep(1)
        
        
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(),fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        canvas.create_text(0,100,text ="将于2秒后开始\n使用说明：\n[1]按住【Ctrl】点击文字可以移动位置\n[2]按【BackSpace】可以重置计时器\n[3]按【ESC】关闭",fill ='#66CCFF',anchor = W,font =('微软雅黑',20))
        canvas.update()
        time.sleep(1)

        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(),fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        canvas.create_text(0,100,text ="将于1秒后开始\n使用说明：\n[1]按住【Ctrl】点击文字可以移动位置\n[2]按【BackSpace】可以重置计时器\n[3]按【ESC】关闭",fill ='#66CCFF',anchor = W,font =('微软雅黑',20))
        canvas.update()
        time.sleep(1)
        #print("从头开始！")
        global i,j,k
        i,j=0,0
        k=time.time()
        while i!=seq[-1][0]:
            refreshText()
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(),fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        canvas.create_text(0,80,text ="运行结束，请重新开始或等待10秒后程序关闭。。。",fill ='#66CCFF',anchor = W,font =('微软雅黑',20))
        canvas.update()
        time.sleep(10)
        exit()

    def control(self):
        #print("去除标题栏失效？")
        tk.overrideredirect(0) #去除标题栏)
    
    def ESC(self):
        tk.withdraw()
        exit()
    
    def ask():
        tk = Tk()
        tk.withdraw()
        AnaData=pd.read_excel(filedialog.askopenfilename())

        AnaData=AnaData.values.tolist()

        global seq
        seq=[]
        for item in AnaData:
            txt=""
            for n in item[3:6]:
                if str(n)!="nan":
                    txt+=str(n)+","
            seq.append([item[0],txt,item[2]]) #seq：0事件，1建造 2农民

        global i,j,k #i：计时器，j：表格中时间的位置，k：起始时间戳
        
        i,j= 0,0

        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win,0)
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(),fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        canvas.create_text(0,100,text ="点击一下文字后，按Backspace键开始\n使用说明：\n[1]按住【Ctrl】点击文字可以移动位置\n[2]按【BackSpace】可以重置计时器\n[3]按【ESC】关闭",fill ='#66CCFF',anchor = W,font =('微软雅黑',20))
        canvas.update()

        tk.mainloop()

    def enter():
        print("小贴士：点击文字按ESC键可以关闭当前悬浮的文字,按Ctrl可以对文字进行移动~")
        print("请输入想要置顶的文字")
        txt=input()
        print("请输入字号")
        tlarge=input()
        print("1s后生成。。")
        time.sleep(1)
        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win,0)
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(),fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        canvas.create_text(0,int(tlarge),text =txt,fill ='#66CCFF',anchor = W,font =('微软雅黑',tlarge))
        canvas.update()
        tk.mainloop()

        

    TRANSCOLOUR = 'gray'
    tk = Tk()
    tk.geometry("800x600+0+0")
    tk.overrideredirect(1) #去除标题栏)
    tk.wm_attributes('-topmost',1)
    tk.title('因为是透明窗体所以不用取title')
    tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
    #tk.resizable(True, True)
        
    #tk.bind('<Configure>', on_resize)
    tk.bind('<Control-space>',control)
    tk.bind('<Control-Alt_L>',withoutcontrol)
    tk.bind('<Control-ButtonPress-1>',draw0)
    tk.bind('<Control-B1-Motion>',draw)
    tk.bind('<Escape>',ESC)

    canvas = Canvas(tk)
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)
    canvas.pack(fill=BOTH, expand=Y)
    canvas.config(highlightthickness=0) #去除画框边缘
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)
    canvas.update()
    if c=='9':
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        canvas.create_text(0,17,text = "Loading。。。",fill ='#66CCFF',anchor = W,font =('微软雅黑',25,'bold'))
        canvas.update()
        tk.bind('<BackSpace>',back)
        ask()
    else:
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        canvas.update()
        enter()
        