from head import *
from Analysis import *
from WhetherFull import *



def AloneRep():
    R = tk.Tk()
    R.withdraw() 
    R.title("选择replay文件")
    res=filedialog.askopenfilename()
    name=os.path.basename(res)
    path=os.path.dirname(res)
    # 获取选择的文件路径
    R.withdraw()
    if not res:
        messagebox.showerror(title='QAQ ~', message="没有选择文件哦")
        sys.exit()
    if res[-9:]!='SC2Replay':
        messagebox.showerror(title='QAQ ~', message="请选择sc2replay文件哦")
        sys.exit()
    print("选取的Rep文件所在的路径是{},伦家会在这里创建Rep分析文件夹哦~".format(path))
    print("开始解析......")

    with alive_bar(11,title='解析进度:') as bar:
        Analysis(res,path,bar)

    if ErrorReport:
        ErrorReportTXT = open("{}/SC2RepAnalysis/{}/ErrorReport.txt".format(path,name), 'w',encoding="utf-8")
        ErrorReportTXT.write(ErrorReport)

    messagebox.showinfo(title='=w= ~', message="txt和excel文件已经生成，位于{}/SC2Analysis/{}".format(path,name))
    os.startfile("{}/SC2RepAnalysis/{}".format(path,name))  
    
def MultiRep():
    print("下面，选择想要分析的reps所在的文件夹吧~")
    R = tk.Tk()
    R.withdraw() 
    R.title("选择replay文件夹")
    dir=filedialog.askdirectory()
    R.withdraw() 

    filesnum=0
    for r,d,f in os.walk(dir):
        for file in f:
            if file[-9:]=="SC2Replay":
                filesnum+=1

    if not dir:
        messagebox.showerror(title='QAQ ~', message="没有选择文件夹哦~")
        sys.exit()            
    if filesnum==0:
        messagebox.showerror(title='QAQ ~', message="选择的文件夹里没有replay文件呀~")
        sys.exit()

    print("选取的录像文件夹所在的路径是{},伦家会在这里创建Rep分析文件夹哦~".format(dir))
    print("当前文件夹中一共有{}个rep文件，开始解析......".format(filesnum))
        
    with alive_bar(11*filesnum,title='批量解析进度:') as bar:
        S=[]
        for r,d,f in os.walk(dir):
            for j in f:
                if j[-9:]=='SC2Replay':
                    bar.text("[{}]".format(j))
                    T=Analysis("{}/{}".format(r,j),dir,bar) 
                    if T:
                        for i in T:
                            S.append(i)

    dirname=os.path.basename(dir)
    S_to_excel = pd.DataFrame(S,columns=['ID','地图','种族','种族对抗',"比赛时间","比赛胜负",'升级顺序','建筑顺序','单位顺序',"rep地址"])
    S_to_excel.to_excel("{}/SC2RepAnalysis/所有对局的建造列表({}目录下).xlsx".format(dir,dirname),index=False)

    if ErrorReport:
        ErrorReportTXT = open('{}/SC2RepAnalysis/{}.txt'.format(dir,"ErrorReport"), 'w',encoding="utf-8")
        ErrorReportTXT.write(ErrorReport)
        ErrorReportTXT.close()

    messagebox.showinfo(title='=w= ~', message="txt和excel文件已经生成，位于{}/SC2Analysis".format(dir))
    os.startfile("{}/SC2RepAnalysis".format(dir))

#---------------------------导入文件------------------------------------#