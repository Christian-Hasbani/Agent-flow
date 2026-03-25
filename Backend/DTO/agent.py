from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class AgentCreate(BaseModel):
    name: str
    role: str
    goal: str
    backstory: str
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    max_iter: int = 20
    allow_delegation: bool = False
    verbose: bool = False


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    goal: Optional[str] = None
    backstory: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    max_iter: Optional[int] = None
    allow_delegation: Optional[bool] = None
    verbose: Optional[bool] = None


class AgentResponse(BaseModel):
    id: UUID4
    name: str
    role: str
    goal: str
    backstory: str
    model: str
    temperature: float
    max_tokens: Optional[int]
    max_iter: int
    allow_delegation: bool
    verbose: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
