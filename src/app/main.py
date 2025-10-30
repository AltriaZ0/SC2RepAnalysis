from app.config import settings
from app.log import setup_logging, LOG
from app.constants import VERSION, UPDATE_DATE
import argparse
from app.analysis.core import analyse_core

def parse_args(argv=None):
    p = argparse.ArgumentParser(prog="app")
    p.add_argument("--log-level", default="INFO")
    sub = p.add_subparsers(dest="cmd", required=True)

    # alone
    s1 = sub.add_parser("alone", help="单回放分析")
    s1.add_argument("--full", action="store_true", help="开启 Full 模式")

    # multi
    s2 = sub.add_parser("multi", help="多回放分析")
    s2.add_argument("--full", action="store_true")

    # train
    s3 = sub.add_parser("train", help="训练")
    s3.add_argument("--kind", choices=["8","9"], required=True)
    return p.parse_args(argv)

def main(argv=None) -> int:
    try:
        setup_logging(settings.log_level)

        LOG.debug("Ciallo～(∠・ω< )⌒★，这里是由AIlian制作的SC2Replay分析工具，欢迎加入sc2萌新吹毛切磋群924040544哟~")
        LOG.info("当前版本{}，更新日期{}".format(VERSION,UPDATE_DATE))
        LOG.info("运行模式:%s, 日志级别:%s", settings.mode, settings.log_level)
        LOG.debug("This is a DEBUG detail (visible only when log_level=DEBUG)")
        # if settings.fulltime == "no":
        #     LOG.info("这其实是一个配置的测试：Fulltime mode not activated.")

        args = parse_args(argv)
        analyse_core(args)

        LOG.info("App exit successfully, bye!")
        return 0
    
    except Exception as e:
        LOG.exception("Unhandled exception: %s", e)
        return 1

if __name__ == "__main__":
   raise SystemExit(main())




