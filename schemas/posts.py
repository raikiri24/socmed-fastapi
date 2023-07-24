from typing import Optional
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    description: Optional[str]
