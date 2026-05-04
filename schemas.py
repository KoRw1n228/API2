from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum
from typing import Optional

class BookStatus(str, Enum):
    AVAILABLE = "наявна"
    ISSUED = "видана"

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    year: int
    status: BookStatus = BookStatus.AVAILABLE

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: UUID