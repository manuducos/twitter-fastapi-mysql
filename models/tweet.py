# Python
from typing import Optional
from datetime import datetime

# Pydantic
from pydantic import BaseModel, Field

# User models
from models.user import UserOut

class TweetIn(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )

class TweetOut(TweetIn):
    id: Optional[int]
    by: UserOut = Field(...)
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)