import json
import random
import time
import uuid
from typing import Any

from fastapi import APIRouter, Request

from app.core.log_config import setup_logging
from app.models import ItemsPublic

log = setup_logging()
router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemsPublic)
def read_items(request: Request) -> Any:
    """
    Retrieve items.
    """
    start_time = time.perf_counter()

    # Log da requisição
    req_info = {
        "method": request.method,
        "url": str(request.url),
        "client": request.client.host,
        "headers": dict(request.headers),
    }
    log.info(f"🔎 Endpoint /items/ chamado | {json.dumps(req_info)}")

    # Processamento
    response = ItemsPublic(user=uuid.uuid4(), random=random.randint(0, 100))

    # Log da resposta
    elapsed = (time.perf_counter() - start_time) * 1000
    resp_info = {
        "user_id": str(response.user),
        "random_number": response.random,
        "elapsed_ms": round(elapsed, 2),
    }
    log.debug(f"✅ Resposta gerada | {json.dumps(resp_info)}")

    return response
