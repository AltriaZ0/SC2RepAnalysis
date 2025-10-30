from .Analysis import Analysis
from app.constants import SC2_SUFFIX
from app.libs import *
from pathlib import Path
from typing import Callable, Iterable, Optional, Dict, Any, List
import logging

LOG = logging.getLogger("app.analysis")

def _is_sc2_replay(path: Path) -> bool:
    # 兼容原逻辑（末尾 9 个字符）+ 更稳妥的后缀判断
    return path.name.endswith("SC2Replay") or path.suffix == SC2_SUFFIX

ProgressCb = Optional[Callable[[str], None]]  # 例如向 Tauri emit 文本

def _emit(progress: ProgressCb, msg: str) -> None:
    if progress:
        try:
            progress(msg)
        except Exception:
            LOG.exception("progress callback failed")

def AloneRep(replay_path:str | Path, output_dir: str | Path, progress: ProgressCb = None) -> None:
    replay_path = Path(replay_path)
    output_dir = Path(output_dir)

    if not replay_path.exists() or not replay_path.is_file():
        raise FileNotFoundError(f"未找到replay文件: {replay_path}")
    if not _is_sc2_replay(replay_path):
        raise ValueError(f"类型无效，请选择 *.SC2Replay 文件: {replay_path}")

    base_dir = replay_path.parent
    name = replay_path.name
    LOG.info("选取的 Rep 文件路径: %s", replay_path)
    LOG.info("将在此目录创建分析输出: %s/SC2RepAnalysis/%s", base_dir, name)
    _emit(progress, f"开始解析: {name}")

    try:
        ret = Analysis(str(replay_path), str(base_dir))
    except Exception as e:
        LOG.exception("解析 replay 失败: %s", replay_path)
        raise e
    
    output_dir.mkdir(parents=True, exist_ok=True)

    msg = f"=w= ~\ntxt和excel文件已经生成，位于: {output_dir}"
    LOG.info(msg)
    _emit(progress, msg)

# def MultiRep():
#     print("下面，选择想要分析的reps所在的文件夹吧~")
#     R = tk.Tk()
#     R.withdraw() 
#     R.title("选择replay文件夹")
#     dir=filedialog.askdirectory()
#     R.withdraw() 

#     filesnum=0
#     for r,d,f in os.walk(dir):
#         for file in f:
#             if file[-9:]=="SC2Replay":
#                 filesnum+=1

#     if not dir:
#         messagebox.showerror(title='QAQ ~', message="没有选择文件夹哦~")
#         sys.exit()            
#     if filesnum==0:
#         messagebox.showerror(title='QAQ ~', message="选择的文件夹里没有replay文件呀~")
#         sys.exit()

#     print("选取的录像文件夹所在的路径是{},伦家会在这里创建Rep分析文件夹哦~".format(dir))
#     print("当前文件夹中一共有{}个rep文件，开始解析......".format(filesnum))
        
#     with alive_bar(11*filesnum,title='批量解析进度:') as bar:
#         S=[]
#         for r,d,f in os.walk(dir):
#             for j in f:
#                 if j[-9:]=='SC2Replay':
#                     bar.text("[{}]".format(j))
#                     T=Analysis("{}/{}".format(r,j),dir,bar) 
#                     if T:
#                         for i in T:
#                             S.append(i)

#     dirname=os.path.basename(dir)
#     S_to_excel = pd.DataFrame(S,columns=['ID','地图','种族','种族对抗',"比赛时间","比赛胜负",'升级顺序','建筑顺序','单位顺序',"rep地址"])
#     S_to_excel.to_excel("{}/SC2RepAnalysis/所有对局的建造列表({}目录下).xlsx".format(dir,dirname),index=False)

#     if ErrorReport:
#         ErrorReportTXT = open('{}/SC2RepAnalysis/{}.txt'.format(dir,"ErrorReport"), 'w',encoding="utf-8")
#         ErrorReportTXT.write(ErrorReport)
#         ErrorReportTXT.close()

#     messagebox.showinfo(title='=w= ~', message="txt和excel文件已经生成，位于{}/SC2Analysis".format(dir))
#     os.startfile("{}/SC2RepAnalysis".format(dir))

#---------------------------导入文件------------------------------------#