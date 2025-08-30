import uuid

from pydantic import BaseModel


class ItemsPublic(BaseModel):
    user: uuid.UUID
    random: int
