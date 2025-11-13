import logging

from logging.handlers import RotatingFileHandler
from app.constants import LOG_DIR
LOG = logging.getLogger("app")  # 本模块（及子模块）公用 logger

def setup_logging(level: str = "INFO") -> None:
    # lvl = getattr(logging, level.upper(), logging.INFO)
    
    # from pathlib import Path
    # log_dir = Path("logs")
    # log_dir.mkdir(exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


    fmt = logging.Formatter(
     fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s", datefmt="%H:%M:%S" 
     )
    # logging.basicConfig(
    #     level=lvl,
    #     format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    #     datefmt="%H:%M:%S",
    # )
    # # 降噪第三方库（按需）
    # logging.getLogger("urllib3").setLevel(logging.WARNING)
    # logging.getLogger("asyncio").setLevel(logging.WARNING)

    # 控制台输出
    # console = logging.StreamHandler()
    # console.setFormatter(fmt)
    # console.setLevel(level)

    # 文件输出（追加模式，utf-8）
    # file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
    # file_handler.setFormatter(fmt)
    # file_handler.setLevel("DEBUG")

    file_handler = RotatingFileHandler(LOG_DIR/"running.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    file_handler.setFormatter(fmt)
    file_handler.setLevel("DEBUG")

    # 清空旧 handler，防止重复输出
    root = logging.getLogger()
    # for h in list(root.handlers):
    #     root.removeHandler(h)

    # root.addHandler(console)
    root.addHandler(file_handler)
    root.setLevel(logging.DEBUG)

