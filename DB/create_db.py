# create_db.py
import enum
import uuid
import os
from sqlalchemy import (
    create_engine, Column, String, Boolean, Float, Integer,
    Text, ForeignKey, Enum, TIMESTAMP, Table
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()


# --- Connection ---
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(DATABASE_URL)

# --- Base ---
class Base(DeclarativeBase):
    pass

# --- Enums ---
class ProcessEnum(str, enum.Enum):
    sequential = "sequential"
    hierarchical = "hierarchical"

class TransportEnum(str, enum.Enum):
    stdio = "stdio"
    sse = "sse"
    http = "http"

class RoleEnum(str, enum.Enum):
    user = "user"
    agent = "agent"


# --- Models ---
class Agent(Base):
    __tablename__ = "agents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    goal = Column(Text)
    backstory = Column(Text)
    model = Column(String, default="gpt-4o")
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, nullable=True)
    max_iter = Column(Integer, default=20)
    allow_delegation = Column(Boolean, default=False)
    verbose = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))

class Crew(Base):
    __tablename__ = "crews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    process = Column(Enum(ProcessEnum), default=ProcessEnum.sequential)
    planning = Column(Boolean, default=False)
    verbose = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))

class McpServer(Base):
    __tablename__ = "mcp_servers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    transport = Column(Enum(TransportEnum), nullable=False)
    command = Column(String, nullable=True)
    args = Column(JSONB, default=list)
    url = Column(String, nullable=True)
    env = Column(JSONB, nullable=True)
    is_global = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crew_id = Column(UUID(as_uuid=True), ForeignKey("crews.id", ondelete="CASCADE"), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=True)
    description = Column(Text)
    expected_output = Column(Text)
    sequence_order = Column(Integer)
    async_execution = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crew_id = Column(UUID(as_uuid=True), ForeignKey("crews.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))

class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    content = Column(Text)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), nullable=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    run_id = Column(UUID(as_uuid=True), nullable=True)
    sequence_order = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True))
    metadata_ = Column("metadata", JSONB, nullable=True)

# --- Junction Tables ---
crew_agents = Table("crew_agents", Base.metadata,
    Column("crew_id", UUID(as_uuid=True), ForeignKey("crews.id", ondelete="CASCADE"), primary_key=True),
    Column("agent_id", UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True),
    Column("is_manager", Boolean, default=False),
)

agent_mcp_servers = Table("agent_mcp_servers", Base.metadata,
    Column("agent_id", UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True),
    Column("mcp_server_id", UUID(as_uuid=True), ForeignKey("mcp_servers.id", ondelete="CASCADE"), primary_key=True),
)

task_context = Table("task_context", Base.metadata,
    Column("task_id", UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("context_task_id", UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
)

# --- Create all tables ---
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("All tables created successfully.")