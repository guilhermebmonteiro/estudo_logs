import random
import uuid
from typing import Any

from fastapi import APIRouter

from app.core.log_config import setup_logging
from app.models import ItemsPublic

log = setup_logging()
router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemsPublic)
def read_items() -> Any:
    """
    Retrieve items.
    """
    log.info("Endpoint /items/ foi chamado")
    response = ItemsPublic(user=uuid.uuid4(), random=random.randint(0, 100))
    return response
