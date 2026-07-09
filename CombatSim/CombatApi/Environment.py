import os
from pathlib import Path
from dataclasses import dataclass


ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def env_flag(name: str, default: bool = False) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    is_prod: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            is_prod=env_flag("IsProd", default=False),
        )


_load_env_file(ENV_PATH)

Config = Settings.from_env()
