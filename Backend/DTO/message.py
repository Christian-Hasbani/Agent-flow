from pydantic import BaseModel, UUID4, Field
from typing import Optional, Literal, Dict, Any
from datetime import datetime


class MessageCreate(BaseModel):
    conversation_id: UUID4
    role: Literal["user", "agent"]
    content: str
    agent_id: Optional[UUID4] = None
    task_id: Optional[UUID4] = None
    run_id: Optional[UUID4] = None
    sequence_order: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = Field(default=None, alias="metadata_")

    model_config = {"populate_by_name": True}


class MessageResponse(BaseModel):
    id: UUID4
    conversation_id: UUID4
    role: str
    content: str
    agent_id: Optional[UUID4]
    task_id: Optional[UUID4]
    run_id: Optional[UUID4]
    sequence_order: Optional[int]
    metadata: Optional[Dict[str, Any]] = Field(default=None, alias="metadata_")
    created_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}
