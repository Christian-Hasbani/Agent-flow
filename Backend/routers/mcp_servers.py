from fastapi import APIRouter, HTTPException
from typing import List

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../DB/services"))
import db_service

from DTO import (
    McpServerCreate, McpServerUpdate, McpServerResponse,
)

router = APIRouter(prefix="/mcp-servers", tags=["MCP Servers"])


@router.get("/", response_model=List[McpServerResponse])
def list_mcp_servers():
    servers = db_service.get_all_mcp_servers()
    return [McpServerResponse.model_validate(s) for s in servers]


@router.get("/global", response_model=List[McpServerResponse])
def list_global_mcp_servers():
    servers = db_service.get_global_mcp_servers()
    return [McpServerResponse.model_validate(s) for s in servers]


@router.get("/{mcp_id}", response_model=McpServerResponse)
def get_mcp_server(mcp_id: str):
    server = db_service.get_mcp_server(mcp_id)
    if not server:
        raise HTTPException(status_code=404, detail="MCP server not found")
    return McpServerResponse.model_validate(server)


@router.post("/", response_model=McpServerResponse, status_code=201)
def create_mcp_server(body: McpServerCreate):
    server = db_service.create_mcp_server(body.model_dump())
    return McpServerResponse.model_validate(server)


@router.patch("/{mcp_id}", response_model=McpServerResponse)
def update_mcp_server(mcp_id: str, body: McpServerUpdate):
    server = db_service.update_mcp_server(
        mcp_id, body.model_dump(exclude_unset=True)
    )
    if not server:
        raise HTTPException(status_code=404, detail="MCP server not found")
    return McpServerResponse.model_validate(server)


@router.delete("/{mcp_id}", status_code=204)
def delete_mcp_server(mcp_id: str):
    deleted = db_service.delete_mcp_server(mcp_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="MCP server not found")
