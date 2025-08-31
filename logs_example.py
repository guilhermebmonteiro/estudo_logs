import sys

from loguru import logger

logger.remove()  # remove handlers padrão

# Configuração do sink padrão
logger.add(
    sys.stderr,
    level="TRACE",  # mostra todos os níveis, porque TRACE é o mais baixo nível
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "  # define o formato
    "<level>{level: <8}</level> | "
    "{file}:{line} | {function}() | {message}",
    colorize=True,  # ativa cores
    backtrace=True,  # quando um erro ocorre, mostra o stack completo
    diagnose=True,  # mostra variáveis locais quando um erro ocorre
    serialize=False,  # não usa JSON
    enqueue=True,  # thread-safe
    catch=True,  # captura erros no logger
)

# Configuração do sink para arquivo
logger.add(
    "logs/logs.json",
    level="TRACE",
    serialize=True,  # gera saída JSON estruturada
    enqueue=True,
    catch=True,
    rotation="10 MB",  # rotation de arquivos grandes
    retention="7 days",  # mantém logs por 7 dias
    compression="zip",  # comprime logs antigos
)

# Exemplos de logs
logger.trace("A trace message.")
logger.debug("A debug message.")
logger.info("An info message.")
logger.success("A success message.")
logger.warning("A warning message.")
logger.error("An error message.")
logger.critical("A critical message.")


def function_name():
    logger.info("Logging from inside a function.")


function_name()
