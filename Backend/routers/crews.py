from fastapi import APIRouter, HTTPException
from typing import List

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../DB/services"))
import db_service

from DTO import (
    CrewCreate, CrewUpdate, CrewResponse,
    AddAgentToCrewRequest,
)

router = APIRouter(prefix="/crews", tags=["Crews"])


@router.get("/", response_model=List[CrewResponse])
def list_crews():
    crews = db_service.get_all_crews()
    return [CrewResponse.model_validate(c) for c in crews]


@router.get("/{crew_id}", response_model=CrewResponse)
def get_crew(crew_id: str):
    crew = db_service.get_crew(crew_id)
    if not crew:
        raise HTTPException(status_code=404, detail="Crew not found")
    return CrewResponse.model_validate(crew)


@router.post("/", response_model=CrewResponse, status_code=201)
def create_crew(body: CrewCreate):
    crew = db_service.create_crew(body.model_dump())
    return CrewResponse.model_validate(crew)


@router.patch("/{crew_id}", response_model=CrewResponse)
def update_crew(crew_id: str, body: CrewUpdate):
    crew = db_service.update_crew(
        crew_id, body.model_dump(exclude_unset=True)
    )
    if not crew:
        raise HTTPException(status_code=404, detail="Crew not found")
    return CrewResponse.model_validate(crew)


@router.delete("/{crew_id}", status_code=204)
def delete_crew(crew_id: str):
    deleted = db_service.delete_crew(crew_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Crew not found")


@router.post("/{crew_id}/agents", status_code=204)
def add_agent_to_crew(crew_id: str, body: AddAgentToCrewRequest):
    db_service.add_agent_to_crew(crew_id, str(body.agent_id), body.is_manager)


@router.delete("/{crew_id}/agents/{agent_id}", status_code=204)
def remove_agent_from_crew(crew_id: str, agent_id: str):
    db_service.remove_agent_from_crew(crew_id, agent_id)
