import random
import uuid
from typing import Any

from fastapi import APIRouter

from app.models import ItemsPublic

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemsPublic)
def read_items() -> Any:
    """
    Retrieve items.
    """
    response = ItemsPublic(user=uuid.uuid4(), random=random.randint(0, 100))
    return response
