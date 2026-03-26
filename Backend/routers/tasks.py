from fastapi import APIRouter, HTTPException
from typing import List

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../DB/services"))
import db_service

from DTO import (
    TaskCreate, TaskUpdate, TaskResponse,
    AddTaskContextRequest,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/crew/{crew_id}", response_model=List[TaskResponse])
def list_tasks_by_crew(crew_id: str):
    tasks = db_service.get_tasks_by_crew(crew_id)
    return [TaskResponse.model_validate(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    task = db_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.model_validate(task)


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(body: TaskCreate):
    task = db_service.create_task(body.model_dump())
    return TaskResponse.model_validate(task)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, body: TaskUpdate):
    task = db_service.update_task(
        task_id, body.model_dump(exclude_unset=True)
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str):
    deleted = db_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")


@router.post("/{task_id}/context", status_code=204)
def add_task_context(task_id: str, body: AddTaskContextRequest):
    db_service.add_task_context(task_id, str(body.context_task_id))


@router.delete("/{task_id}/context/{context_task_id}", status_code=204)
def remove_task_context(task_id: str, context_task_id: str):
    db_service.remove_task_context(task_id, context_task_id)
