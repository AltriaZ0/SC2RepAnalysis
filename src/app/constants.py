import tomli as tomllib
from pathlib import Path

# 路径类常量（以 Path 表示更安全）
BASE_DIR = Path(__file__).resolve().parents[1]

LOG_DIR = BASE_DIR / "logs"

PARENT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PARENT_DIR / "data"

# 项目信息常量
with open( PARENT_DIR / "pyproject.toml", "rb") as f:
    pyproject_data = tomllib.load(f)
    
NAME = pyproject_data["project"]["name"]
VERSION = pyproject_data["project"]["version"]
UPDATE_DATE = pyproject_data["project"]["date-updated"]

# 网络常量
DEFAULT_PORT = 8080
DEFAULT_HOST = "127.0.0.1"
# 后缀名常量
SC2_SUFFIX = ".SC2Replay" 