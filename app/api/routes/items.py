import random
import time
import uuid
from typing import Any

from fastapi import APIRouter, Request

from app.core.logging_config import setup_logging as setup_std_logging

# duas configs diferentes
from app.core.loguru_config import setup_logging as setup_loguru
from app.models import ItemsPublic

# inicializa ambos
log_loguru = setup_loguru()
log_logging = setup_std_logging()

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/loguru", response_model=ItemsPublic)
def read_items_loguru(request: Request) -> Any:
    """
    Teste de logging com Loguru
    """
    start_time = time.perf_counter()

    # log da requisição
    req_info = {  # noqa: F841
        "method": request.method,
        "url": str(request.url),
        "client": request.client.host,
        "headers": dict(request.headers),
    }
    log_loguru.info("🔎 Endpoint /items/loguru chamado")
    log_loguru.error("ERRO Endpoint /items/loguru chamado")

    # processamento
    response = ItemsPublic(user=uuid.uuid4(), random=random.randint(0, 100))

    # log da resposta
    elapsed = (time.perf_counter() - start_time) * 1000
    resp_info = {  # noqa: F841
        "user_id": str(response.user),
        "random_number": response.random,
        "elapsed_ms": round(elapsed, 2),
    }
    log_loguru.debug("✅ Resposta gerada ")

    return response


@router.get("/logging", response_model=ItemsPublic)
def read_items_logging(request: Request) -> Any:
    """
    Teste de logging com logging nativo
    """
    start_time = time.perf_counter()

    # log da requisição
    req_info = {  # noqa: F841
        "method": request.method,
        "url": str(request.url),
        "client": request.client.host,
        "headers": dict(request.headers),
    }
    log_logging.info("🔎 Endpoint /items/logging chamado")
    log_logging.error("ERRO Endpoint /items/logging chamado")

    # processamento
    response = ItemsPublic(user=uuid.uuid4(), random=random.randint(0, 100))

    # log da resposta
    elapsed = (time.perf_counter() - start_time) * 1000
    resp_info = {  # noqa: F841
        "user_id": str(response.user),
        "random_number": response.random,
        "elapsed_ms": round(elapsed, 2),
    }
    log_logging.debug("✅ Resposta gerada")

    return response
