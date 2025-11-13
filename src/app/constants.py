import sys,tomli as tomllib
from pathlib import Path

# 路径类常量（以 Path 表示更安全）

if getattr(sys, "frozen", False):
    # exe 模式：exe 所在目录
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # 源码模式
    BASE_DIR = Path(__file__).resolve().parents[2]
    
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

# 项目信息常量
# with open( BASE_DIR / "pyproject.toml", "rb") as f:
#     pyproject_data = tomllib.load(f)
    
# NAME = pyproject_data["project"]["name"]
# VERSION = pyproject_data["project"]["version"]
# UPDATE_DATE = pyproject_data["project"]["date-updated"]

NAME = "SC2RepAnalysis"
VERSION = "1.4.0"
UPDATE_DATE = "2025-11-09"

# 网络常量
DEFAULT_PORT = 8080
DEFAULT_HOST = "127.0.0.1"
# 后缀名常量
SC2_SUFFIX = ".SC2Replay" 