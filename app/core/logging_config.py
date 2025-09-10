import json
import logging
import logging.handlers
import time
from pathlib import Path
from typing import ClassVar

import httpx

from app.core.config import settings


def mask_sensitive(value: str, show_last: int = 2) -> str:
    """Mascarar valor sensível, mantendo apenas os últimos caracteres."""
    if not value:
        return value
    masked_len = len(value) - show_last
    if masked_len <= 0:
        return "*" * len(value)
    return "*" * masked_len + value[-show_last:]


class LokiHandler(logging.Handler):
    def emit(self, record):
        try:
            timestamp = str(int(time.time() * 1_000_000_000))  # nanosegundos
            log_line = self.format(record)

            labels = {
                "language": "python",
                "source": "fastapi",
                "level": record.levelname,
                "file": record.filename,
                "function": record.funcName,
            }

            payload = {
                "streams": [
                    {
                        "stream": labels,
                        "values": [[timestamp, log_line]],
                    }
                ]
            }

            headers = {"Content-Type": "application/json"}
            resp = httpx.post(
                url=settings.LOKI_URL,
                auth=(settings.LOKI_USER_ID, settings.LOKI_TOKEN),
                json=payload,
                headers=headers,
                timeout=5.0,
            )
            resp.raise_for_status()
        except Exception:
            self.handleError(record)


class ColorFormatter(logging.Formatter):
    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[94m",  # azul
        "INFO": "\033[92m",  # verde
        "WARNING": "\033[93m",  # amarelo
        "ERROR": "\033[91m",  # vermelho
        "CRITICAL": "\033[95m",  # magenta
    }
    RESET: ClassVar[str] = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        msg = super().format(record)
        return f"{color}{msg}{self.RESET}"


def setup_logging():
    logger = logging.getLogger("myapp")
    if logger.handlers:  # se já tiver handlers, retorna
        return logger
    logger.setLevel(logging.DEBUG)

    base_fmt = logging.Formatter(
        (
            "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | "
            "%(funcName)s() | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        ColorFormatter(base_fmt._fmt, base_fmt.datefmt)
    )

    # --- File handler (JSON rotacionado) ---
    Path("logs").mkdir(exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        "logs/logs.json",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=7,
    )
    file_handler.setLevel(logging.INFO)

    # serializa log em JSON
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "time": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                "file": record.filename,
                "line": record.lineno,
                "function": record.funcName,
                "message": record.getMessage(),
            }
            return json.dumps(log_record)

    file_handler.setFormatter(JsonFormatter())

    # --- Loki handler ---
    loki_handler = LokiHandler()
    loki_handler.setLevel(logging.INFO)
    loki_handler.setFormatter(base_fmt)

    # adiciona todos handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(loki_handler)

    return logger
