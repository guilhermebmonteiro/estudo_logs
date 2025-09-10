import sys
import time

import httpx
from loguru import logger

from app.core.config import settings


def send_log_to_loki(record: dict):
    """Send log to loki."""
    timestamp = str(int(time.time() * 1_000_000_000))  # nanoseconds

    # building labels to Loki
    labels = {
        "language": "python",
        "source": "fastapi",
        "level": record["level"].name,
        "file": record["file"].name,
        "function": record["function"],
    }
    # logging line format
    log_line = (
        f"{record['time'].strftime('%Y-%m-%d %H:%M:%S')} | "
        f"{record['level'].name:<8} | "
        f"{record['file'].name}:{record['line']} | {record['function']}() | "
        f"{record['message']}"
    )

    payload = {
        "streams": [
            {
                "stream": labels,
                "values": [[timestamp, log_line]],
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    try:
        resp = httpx.post(
            url=settings.LOKI_URL,
            auth=(settings.LOKI_USER_ID, settings.LOKI_TOKEN),
            json=payload,
            headers=headers,
            timeout=5.0,
        )
        resp.raise_for_status()
    except httpx.RequestException as e:
        logger.opt(exception=True).error(f"Erro ao enviar log para Loki: {e}")


def setup_logging():
    # remove default
    logger.remove()

    # terminal sink
    logger.add(
        sys.stderr,
        level="TRACE",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "{file}:{line} | {function}() | {message}",
        colorize=True,
        backtrace=True,
        diagnose=True,
        enqueue=True,
        catch=True,
    )

    # json file sink
    logger.add(
        "logs/logs.json",
        level="INFO",
        serialize=True,
        enqueue=True,
        catch=True,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )

    # third sink -> send to Loki
    def loguru_to_loki(message):
        send_log_to_loki(message.record)

    logger.add(loguru_to_loki, level="INFO", enqueue=True, catch=True)
    return logger
