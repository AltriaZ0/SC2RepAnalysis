from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class AppSettings(BaseSettings):
    mode: Literal["local", "remote"] = "local"
    # 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    # 新增字段 fulltime，只能是 0 或 1
    fulltime: Literal["yes","no"] = "no"

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        # 可选：嵌套字段用双下划线映射，例如 APP_LOG__LEVEL
        # env_nested_delimiter="__",
    )

settings = AppSettings()