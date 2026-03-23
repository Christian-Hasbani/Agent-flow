import sys
import os
import uuid
from datetime import datetime, timezone

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.orm import Session
from create_db import (
    engine,
    Agent, Crew, McpServer, Task, Conversation, Message,
    crew_agents, agent_mcp_servers, task_context,
)


def _now():
    return datetime.now(timezone.utc)


def _session() -> Session:
    return Session(engine)


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

def get_agent(agent_id: str):
    with _session() as s:
        return s.get(Agent, uuid.UUID(agent_id))


def get_all_agents():
    with _session() as s:
        return s.query(Agent).all()


def create_agent(data: dict) -> Agent:
    with _session() as s:
        agent = Agent(id=uuid.uuid4(), created_at=_now(), updated_at=_now(), **data)
        s.add(agent)
        s.commit()
        s.refresh(agent)
        return agent


def update_agent(agent_id: str, data: dict) -> Agent | None:
    with _session() as s:
        agent = s.get(Agent, uuid.UUID(agent_id))
        if not agent:
            return None
        for key, value in data.items():
            setattr(agent, key, value)
        agent.updated_at = _now()
        s.commit()
        s.refresh(agent)
        return agent


def delete_agent(agent_id: str) -> bool:
    with _session() as s:
        agent = s.get(Agent, uuid.UUID(agent_id))
        if not agent:
            return False
        s.delete(agent)
        s.commit()
        return True


# ---------------------------------------------------------------------------
# Crews
# ---------------------------------------------------------------------------

def get_crew(crew_id: str):
    with _session() as s:
        return s.get(Crew, uuid.UUID(crew_id))


def get_all_crews():
    with _session() as s:
        return s.query(Crew).all()


def create_crew(data: dict) -> Crew:
    with _session() as s:
        crew = Crew(id=uuid.uuid4(), created_at=_now(), updated_at=_now(), **data)
        s.add(crew)
        s.commit()
        s.refresh(crew)
        return crew


def update_crew(crew_id: str, data: dict) -> Crew | None:
    with _session() as s:
        crew = s.get(Crew, uuid.UUID(crew_id))
        if not crew:
            return None
        for key, value in data.items():
            setattr(crew, key, value)
        crew.updated_at = _now()
        s.commit()
        s.refresh(crew)
        return crew


def delete_crew(crew_id: str) -> bool:
    with _session() as s:
        crew = s.get(Crew, uuid.UUID(crew_id))
        if not crew:
            return False
        s.delete(crew)
        s.commit()
        return True


def add_agent_to_crew(crew_id: str, agent_id: str, is_manager: bool = False):
    with _session() as s:
        s.execute(
            crew_agents.insert().values(
                crew_id=uuid.UUID(crew_id),
                agent_id=uuid.UUID(agent_id),
                is_manager=is_manager,
            )
        )
        s.commit()


def remove_agent_from_crew(crew_id: str, agent_id: str):
    with _session() as s:
        s.execute(
            crew_agents.delete().where(
                crew_agents.c.crew_id == uuid.UUID(crew_id),
                crew_agents.c.agent_id == uuid.UUID(agent_id),
            )
        )
        s.commit()


def get_crew_agents(crew_id: str):
    with _session() as s:
        rows = s.execute(
            crew_agents.select().where(crew_agents.c.crew_id == uuid.UUID(crew_id))
        ).fetchall()
        return rows


# ---------------------------------------------------------------------------
# MCP Servers
# ---------------------------------------------------------------------------

def get_mcp_server(mcp_id: str):
    with _session() as s:
        return s.get(McpServer, uuid.UUID(mcp_id))


def get_all_mcp_servers():
    with _session() as s:
        return s.query(McpServer).all()


def get_global_mcp_servers():
    with _session() as s:
        return s.query(McpServer).filter(McpServer.is_global == True).all()


def create_mcp_server(data: dict) -> McpServer:
    with _session() as s:
        mcp = McpServer(id=uuid.uuid4(), created_at=_now(), updated_at=_now(), **data)
        s.add(mcp)
        s.commit()
        s.refresh(mcp)
        return mcp


def update_mcp_server(mcp_id: str, data: dict) -> McpServer | None:
    with _session() as s:
        mcp = s.get(McpServer, uuid.UUID(mcp_id))
        if not mcp:
            return None
        for key, value in data.items():
            setattr(mcp, key, value)
        mcp.updated_at = _now()
        s.commit()
        s.refresh(mcp)
        return mcp


def delete_mcp_server(mcp_id: str) -> bool:
    with _session() as s:
        mcp = s.get(McpServer, uuid.UUID(mcp_id))
        if not mcp:
            return False
        s.delete(mcp)
        s.commit()
        return True


def assign_mcp_to_agent(agent_id: str, mcp_server_id: str):
    with _session() as s:
        s.execute(
            agent_mcp_servers.insert().values(
                agent_id=uuid.UUID(agent_id),
                mcp_server_id=uuid.UUID(mcp_server_id),
            )
        )
        s.commit()


def remove_mcp_from_agent(agent_id: str, mcp_server_id: str):
    with _session() as s:
        s.execute(
            agent_mcp_servers.delete().where(
                agent_mcp_servers.c.agent_id == uuid.UUID(agent_id),
                agent_mcp_servers.c.mcp_server_id == uuid.UUID(mcp_server_id),
            )
        )
        s.commit()


def get_agent_mcp_servers(agent_id: str):
    with _session() as s:
        rows = s.execute(
            agent_mcp_servers.select().where(
                agent_mcp_servers.c.agent_id == uuid.UUID(agent_id)
            )
        ).fetchall()
        return rows


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

def get_task(task_id: str):
    with _session() as s:
        return s.get(Task, uuid.UUID(task_id))


def get_tasks_by_crew(crew_id: str):
    with _session() as s:
        return (
            s.query(Task)
            .filter(Task.crew_id == uuid.UUID(crew_id))
            .order_by(Task.sequence_order)
            .all()
        )


def create_task(data: dict) -> Task:
    with _session() as s:
        task = Task(id=uuid.uuid4(), created_at=_now(), updated_at=_now(), **data)
        s.add(task)
        s.commit()
        s.refresh(task)
        return task


def update_task(task_id: str, data: dict) -> Task | None:
    with _session() as s:
        task = s.get(Task, uuid.UUID(task_id))
        if not task:
            return None
        for key, value in data.items():
            setattr(task, key, value)
        task.updated_at = _now()
        s.commit()
        s.refresh(task)
        return task


def delete_task(task_id: str) -> bool:
    with _session() as s:
        task = s.get(Task, uuid.UUID(task_id))
        if not task:
            return False
        s.delete(task)
        s.commit()
        return True


def add_task_context(task_id: str, context_task_id: str):
    with _session() as s:
        s.execute(
            task_context.insert().values(
                task_id=uuid.UUID(task_id),
                context_task_id=uuid.UUID(context_task_id),
            )
        )
        s.commit()


def remove_task_context(task_id: str, context_task_id: str):
    with _session() as s:
        s.execute(
            task_context.delete().where(
                task_context.c.task_id == uuid.UUID(task_id),
                task_context.c.context_task_id == uuid.UUID(context_task_id),
            )
        )
        s.commit()


def get_task_contexts(task_id: str):
    with _session() as s:
        rows = s.execute(
            task_context.select().where(task_context.c.task_id == uuid.UUID(task_id))
        ).fetchall()
        return rows


# ---------------------------------------------------------------------------
# Conversations
# ---------------------------------------------------------------------------

def get_conversation(conversation_id: str):
    with _session() as s:
        return s.get(Conversation, uuid.UUID(conversation_id))


def get_conversations_by_crew(crew_id: str):
    with _session() as s:
        return (
            s.query(Conversation)
            .filter(Conversation.crew_id == uuid.UUID(crew_id))
            .order_by(Conversation.created_at.desc())
            .all()
        )


def create_conversation(data: dict) -> Conversation:
    with _session() as s:
        conversation = Conversation(id=uuid.uuid4(), created_at=_now(), updated_at=_now(), **data)
        s.add(conversation)
        s.commit()
        s.refresh(conversation)
        return conversation


def update_conversation(conversation_id: str, data: dict) -> Conversation | None:
    with _session() as s:
        conversation = s.get(Conversation, uuid.UUID(conversation_id))
        if not conversation:
            return None
        for key, value in data.items():
            setattr(conversation, key, value)
        conversation.updated_at = _now()
        s.commit()
        s.refresh(conversation)
        return conversation


def delete_conversation(conversation_id: str) -> bool:
    with _session() as s:
        conversation = s.get(Conversation, uuid.UUID(conversation_id))
        if not conversation:
            return False
        s.delete(conversation)
        s.commit()
        return True


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------

def get_message(message_id: str):
    with _session() as s:
        return s.get(Message, uuid.UUID(message_id))


def get_messages_by_conversation(conversation_id: str):
    with _session() as s:
        return (
            s.query(Message)
            .filter(Message.conversation_id == uuid.UUID(conversation_id))
            .order_by(Message.sequence_order)
            .all()
        )


def get_messages_by_run(run_id: str):
    with _session() as s:
        return (
            s.query(Message)
            .filter(Message.run_id == uuid.UUID(run_id))
            .order_by(Message.sequence_order)
            .all()
        )


def create_message(data: dict) -> Message:
    with _session() as s:
        message = Message(id=uuid.uuid4(), created_at=_now(), **data)
        s.add(message)
        s.commit()
        s.refresh(message)
        return message


def delete_message(message_id: str) -> bool:
    with _session() as s:
        message = s.get(Message, uuid.UUID(message_id))
        if not message:
            return False
        s.delete(message)
        s.commit()
        return True


def delete_messages_by_conversation(conversation_id: str):
    with _session() as s:
        s.query(Message).filter(
            Message.conversation_id == uuid.UUID(conversation_id)
        ).delete()
        s.commit()
