import sys

from loguru import logger


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

    # json file sink, good for Loki
    logger.add(
        "logs.json",
        level="INFO",  # geralmente Loki consome INFO+
        serialize=True,  # JSON estruturado
        enqueue=True,
        catch=True,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )

    return logger
