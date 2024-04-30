from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BaseTextDTO(BaseModel):
    title: str
    text: str
    kirillic_text: Optional[str]
    image: str
    comment: str

    class Config:
        orm_mode = True

class TextUpdateDTO(BaseTextDTO):
    id: int
    title: Optional[str]
    text: Optional[str]
    image: Optional[str]

class TextDTO(BaseTextDTO):
    id: int
    created_at: datetime