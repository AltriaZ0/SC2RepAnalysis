from .putin import *
from .Analysis import *
from .file_io import *

# 分析功能的入口，选择处理分支

def analyse_core(args=None):
    """分析核心函数，根据命令行参数调用相应的分析功能"""
    if args.cmd == "alone":
        # AloneRep(args.full)
        rep_path = get_replay_path()
        AloneRep(rep_path, Path(rep_path).parent/"SC2RepAnalysis", None)
    elif args.cmd == "multi":
        rep_dir = get_replay_dir()
        MultiRep(rep_dir, Path(rep_dir).parent/"SC2RepAnalysis", None)
