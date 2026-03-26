from pydantic import BaseModel, UUID4
from typing import Optional, Literal, Dict, Any
from datetime import datetime


class McpServerCreate(BaseModel):
    name: str
    description: Optional[str] = None
    transport: Literal["stdio", "sse", "http"]
    command: Optional[str] = None
    args: Optional[list] = None
    url: Optional[str] = None
    env: Optional[Dict[str, Any]] = None
    is_global: bool = False


class McpServerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    transport: Optional[Literal["stdio", "sse", "http"]] = None
    command: Optional[str] = None
    args: Optional[list] = None
    url: Optional[str] = None
    env: Optional[Dict[str, Any]] = None
    is_global: Optional[bool] = None


class McpServerResponse(BaseModel):
    id: UUID4
    name: str
    description: Optional[str]
    transport: str
    command: Optional[str]
    args: Optional[list]
    url: Optional[str]
    is_global: bool
    # env is intentionally excluded — never return secrets to the client
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
