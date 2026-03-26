from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    name: Optional[str] = None
    description: str
    expected_output: str
    crew_id: UUID4
    agent_id: UUID4
    sequence_order: Optional[int] = None
    async_execution: bool = False


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    expected_output: Optional[str] = None
    agent_id: Optional[UUID4] = None
    crew_id: Optional[UUID4] = None
    sequence_order: Optional[int] = None
    async_execution: Optional[bool] = None


class TaskResponse(BaseModel):
    id: UUID4
    name: Optional[str]
    description: str
    expected_output: str
    crew_id: UUID4
    agent_id: UUID4
    sequence_order: Optional[int]
    async_execution: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AddTaskContextRequest(BaseModel):
    context_task_id: UUID4
