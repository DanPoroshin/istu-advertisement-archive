from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BaseTextDTO(BaseModel):
    id: int
    title: str
    image: str

    class Config:
        from_attributes = True


class TextUpdateDTO(BaseTextDTO):
    title: Optional[str]
    text: Optional[str]
    image: Optional[str]
    kirillic_text: Optional[str]


class TextDTO(BaseTextDTO):
    text: str
    kirillic_text: Optional[str]
    comment: str
    created_at: datetime
