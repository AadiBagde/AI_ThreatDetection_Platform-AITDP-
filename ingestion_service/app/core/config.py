import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = "AITDP Ingestion Service"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            app_version=os.getenv("APP_VERSION", cls.app_version),
            debug=os.getenv("DEBUG", "false").lower() in ("1", "true", "yes"),
            log_level=os.getenv("LOG_LEVEL", cls.log_level).upper(),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()
