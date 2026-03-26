from pydantic import BaseModel, UUID4
from typing import Optional, Literal
from datetime import datetime


class CrewCreate(BaseModel):
    name: str
    description: Optional[str] = None
    process: Literal["sequential", "hierarchical"] = "hierarchical"
    planning: bool = False
    verbose: bool = False


class CrewUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    process: Optional[Literal["sequential", "hierarchical"]] = None
    planning: Optional[bool] = None
    verbose: Optional[bool] = None


class CrewResponse(BaseModel):
    id: UUID4
    name: str
    description: Optional[str]
    process: str
    planning: bool
    verbose: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AddAgentToCrewRequest(BaseModel):
    agent_id: UUID4
    is_manager: bool = False
