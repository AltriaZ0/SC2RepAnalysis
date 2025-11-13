from .Analysis import ReplayAnalyzer
from app.constants import SC2_SUFFIX
from app.libsK import *
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

    # base_dir = replay_path.parent
    name = replay_path.name
    LOG.info("选取的 Rep 文件路径: %s", replay_path)
    LOG.info("将在此目录创建分析输出: %s\SC2RepAnalysis\%s", output_dir, name)
    _emit(progress, f"开始解析: {name}")

    try:
        analyzer = ReplayAnalyzer(str(replay_path), output_dir)
        result = analyzer.analyze() 
    except Exception as e:
        LOG.exception("解析 replay 失败: %s", replay_path)
        raise e
    


    msg = f"=w= ~\ntxt和excel文件已经生成，位于: {output_dir}"
    LOG.info(msg)
    _emit(progress, msg)
    return result

def MultiRep(replay_dir:str | Path, output_dir: str | Path, progress: ProgressCb = None) -> None:
    replay_dir = Path(replay_dir)
    output_dir = Path(output_dir)
    summary_dir = output_dir / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    LOG.info("replay_dir:%s",replay_dir)

    S=[]
    for r,d,f in os.walk(replay_dir):
        for j in f:
            if j[-9:]=='SC2Replay':
                T=ReplayAnalyzer("{}/{}".format(r,j),output_dir) 
                T.analyze()
                result = T.PdS
                if T:
                    for i in result:
                        S.append(i)

    dirname=os.path.basename(replay_dir)
    
    S_to_excel = pd.DataFrame(S,columns=['ID','地图','种族','种族对抗',"比赛时间","比赛胜负",'升级顺序','建筑顺序','单位顺序',"rep地址"])
    S_to_excel.to_excel("{}/summary/所有对局的建造列表({}目录下).xlsx".format(output_dir,dirname),index=False)

    LOG.info("txt和excel文件已经生成，位于{}".format(output_dir))
    os.startfile("{}".format(output_dir))
