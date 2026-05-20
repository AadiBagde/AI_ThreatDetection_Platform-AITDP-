import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = "AITDP ML Engine"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"
    host: str = "127.0.0.1"
    port: int = 8002
    model_dir: str = "models/trained"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("ML_APP_NAME", cls.app_name),
            app_version=os.getenv("ML_APP_VERSION", cls.app_version),
            debug=os.getenv("DEBUG", "false").lower() in ("1", "true", "yes"),
            log_level=os.getenv("LOG_LEVEL", cls.log_level).upper(),
            host=os.getenv("ML_HOST", cls.host),
            port=int(os.getenv("ML_PORT", str(cls.port))),
            model_dir=os.getenv("MODEL_DIR", cls.model_dir),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()
