from fastapi import APIRouter, HTTPException
from typing import List

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../DB/services"))
import db_service

from DTO import (
    ConversationCreate, ConversationUpdate, ConversationResponse,
)

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get("/crew/{crew_id}", response_model=List[ConversationResponse])
def list_conversations_by_crew(crew_id: str):
    conversations = db_service.get_conversations_by_crew(crew_id)
    return [ConversationResponse.model_validate(c) for c in conversations]


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: str):
    conversation = db_service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationResponse.model_validate(conversation)


@router.post("/", response_model=ConversationResponse, status_code=201)
def create_conversation(body: ConversationCreate):
    conversation = db_service.create_conversation(body.model_dump())
    return ConversationResponse.model_validate(conversation)


@router.patch("/{conversation_id}", response_model=ConversationResponse)
def update_conversation(conversation_id: str, body: ConversationUpdate):
    conversation = db_service.update_conversation(
        conversation_id, body.model_dump(exclude_unset=True)
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationResponse.model_validate(conversation)


@router.delete("/{conversation_id}", status_code=204)
def delete_conversation(conversation_id: str):
    deleted = db_service.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
