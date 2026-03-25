from fastapi import APIRouter, HTTPException
from typing import List

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../DB/services"))
import db_service

from DTO import (
    AgentCreate, AgentUpdate, AgentResponse,
)

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("/", response_model=List[AgentResponse])
def list_agents():
    agents = db_service.get_all_agents()
    return [AgentResponse.model_validate(a) for a in agents]


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: str):
    agent = db_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentResponse.model_validate(agent)


@router.post("/", response_model=AgentResponse, status_code=201)
def create_agent(body: AgentCreate):
    agent = db_service.create_agent(body.model_dump())
    return AgentResponse.model_validate(agent)


@router.patch("/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: str, body: AgentUpdate):
    agent = db_service.update_agent(
        agent_id, body.model_dump(exclude_unset=True)
    )
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentResponse.model_validate(agent)


@router.delete("/{agent_id}", status_code=204)
def delete_agent(agent_id: str):
    deleted = db_service.delete_agent(agent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/{agent_id}/mcp-servers/{mcp_server_id}", status_code=204)
def assign_mcp_to_agent(agent_id: str, mcp_server_id: str):
    db_service.assign_mcp_to_agent(agent_id, mcp_server_id)


@router.delete("/{agent_id}/mcp-servers/{mcp_server_id}", status_code=204)
def remove_mcp_from_agent(agent_id: str, mcp_server_id: str):
    db_service.remove_mcp_from_agent(agent_id, mcp_server_id)
