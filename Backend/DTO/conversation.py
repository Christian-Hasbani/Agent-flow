from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class ConversationCreate(BaseModel):
    crew_id: UUID4
    title: Optional[str] = None


class ConversationUpdate(BaseModel):
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    id: UUID4
    crew_id: UUID4
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
