from fastapi import APIRouter, HTTPException
from typing import List

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../DB/services"))
import db_service

from DTO import MessageCreate, MessageResponse

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/conversation/{conversation_id}", response_model=List[MessageResponse])
def list_messages_by_conversation(conversation_id: str):
    messages = db_service.get_messages_by_conversation(conversation_id)
    return [MessageResponse.model_validate(m) for m in messages]


@router.get("/run/{run_id}", response_model=List[MessageResponse])
def list_messages_by_run(run_id: str):
    messages = db_service.get_messages_by_run(run_id)
    return [MessageResponse.model_validate(m) for m in messages]


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(message_id: str):
    message = db_service.get_message(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return MessageResponse.model_validate(message)


@router.post("/", response_model=MessageResponse, status_code=201)
def create_message(body: MessageCreate):
    data = body.model_dump(by_alias=True)
    message = db_service.create_message(data)
    return MessageResponse.model_validate(message)


@router.delete("/{message_id}", status_code=204)
def delete_message(message_id: str):
    deleted = db_service.delete_message(message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Message not found")
