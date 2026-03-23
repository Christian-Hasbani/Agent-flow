# Agent-flow
AgentFlow is an platform for building and orchestrating multi-agent AI systems, featuring a ChatGPT-like interface where you can create custom AI agents, let them collaborate with each other in real time, and connect them to external tools and services through MCP servers.


# Architecture
UI: chatgpt clone
DB: 
- Memory Redis
- chats (+ userID optional) Postgres 
- Agents Postgres
Backend: 
- Hybrid Agents
- Hybrid MCP
- CRUD operations


## PostgreSQL Schema

### `agents` ← maps to CrewAI `Agent`

| Column             | Type          | Notes                                    |
| ------------------ | ------------- | ---------------------------------------- |
| `id`               | `UUID PK`     |                                          |
| `name`             | `VARCHAR`     | display name                             |
| `role`             | `VARCHAR`     | CrewAI `role` — defines expertise        |
| `goal`             | `TEXT`        | CrewAI `goal` — guides decisions         |
| `backstory`        | `TEXT`        | CrewAI `backstory` — personality/context |
| `model`            | `VARCHAR`     | default `gpt-4o`                         |
| `temperature`      | `FLOAT`       | default `0.7`                            |
| `max_tokens`       | `INT`         | nullable                                 |
| `max_iter`         | `INT`         | default `20` — max reasoning iterations  |
| `allow_delegation` | `BOOL`        | default `false`                          |
| `verbose`          | `BOOL`        | default `false`                          |
| `created_at`       | `TIMESTAMPTZ` |                                          |
| `updated_at`       | `TIMESTAMPTZ` |                                          |

---

### `crews` ← maps to CrewAI `Crew`

| Column        | Type          | Notes                                               |
| ------------- | ------------- | --------------------------------------------------- |
| `id`          | `UUID PK`     |                                                     |
| `name`        | `VARCHAR`     |                                                     |
| `description` | `TEXT`        | nullable                                            |
| `process`     | `ENUM`        | `sequential`, `hierarchical` — default `sequential` |
| `planning`    | `BOOL`        | enables CrewAI's AgentPlanner before execution      |
| `verbose`     | `BOOL`        | default `false`                                     |
| `created_at`  | `TIMESTAMPTZ` |                                                     |
| `updated_at`  | `TIMESTAMPTZ` |                                                     |

---

### `crew_agents` _(junction)_

| Column       | Type                  | Notes                                              |
| ------------ | --------------------- | -------------------------------------------------- |
| `crew_id`    | `UUID FK → crews`     |                                                    |
| `agent_id`   | `UUID FK → agents`    |                                                    |
| `is_manager` | `BOOL`                | for hierarchical process — marks the manager agent |
| **PK**       | `(crew_id, agent_id)` |                                                    |

---

### `tasks` ← maps to CrewAI `Task`

| Column            | Type               | Notes                            |
| ----------------- | ------------------ | -------------------------------- |
| `id`              | `UUID PK`          |                                  |
| `crew_id`         | `UUID FK → crews`  |                                  |
| `agent_id`        | `UUID FK → agents` | the agent assigned to this task  |
| `name`            | `VARCHAR`          | optional identifier              |
| `description`     | `TEXT`             | what the task entails            |
| `expected_output` | `TEXT`             | what a completed task looks like |
| `sequence_order`  | `INT`              | execution order within the crew  |
| `async_execution` | `BOOL`             | default `false`                  |
| `created_at`      | `TIMESTAMPTZ`      |                                  |
| `updated_at`      | `TIMESTAMPTZ`      |                                  |

---

### `task_context` _(self-referential junction)_

When a task needs the output of another task as context (CrewAI `context=[]`).

| Column            | Type                         | Notes                         |
| ----------------- | ---------------------------- | ----------------------------- |
| `task_id`         | `UUID FK → tasks`            | the task that needs context   |
| `context_task_id` | `UUID FK → tasks`            | the task whose output is used |
| **PK**            | `(task_id, context_task_id)` |                               |

---

### `mcp_servers` ← CrewAI `tools`

| Column        | Type          | Notes                                         |
| ------------- | ------------- | --------------------------------------------- |
| `id`          | `UUID PK`     |                                               |
| `name`        | `VARCHAR`     |                                               |
| `description` | `TEXT`        | nullable                                      |
| `transport`   | `ENUM`        | `stdio`, `sse`, `http`                        |
| `command`     | `VARCHAR`     | nullable — for `stdio`                        |
| `args`        | `JSONB`       | default `[]`                                  |
| `url`         | `VARCHAR`     | nullable — for `sse`/`http`                   |
| `env`         | `JSONB`       | nullable — move secrets out before production |
| `is_global`   | `BOOL`        | available to all agents if `true`             |
| `created_at`  | `TIMESTAMPTZ` |                                               |
| `updated_at`  | `TIMESTAMPTZ` |                                               |

---

### `agent_mcp_servers` _(junction)_

| Column          | Type                        | Notes |
| --------------- | --------------------------- | ----- |
| `agent_id`      | `UUID FK → agents`          |       |
| `mcp_server_id` | `UUID FK → mcp_servers`     |       |
| **PK**          | `(agent_id, mcp_server_id)` |       |

---

### `conversations`

| Column       | Type              | Notes                                |
| ------------ | ----------------- | ------------------------------------ |
| `id`         | `UUID PK`         |                                      |
| `crew_id`    | `UUID FK → crews` | which crew handles this conversation |
| `title`      | `VARCHAR`         | nullable                             |
| `created_at` | `TIMESTAMPTZ`     |                                      |
| `updated_at` | `TIMESTAMPTZ`     |                                      |

---

### `messages`

| Column            | Type                      | Notes                                                          |
| ----------------- | ------------------------- | -------------------------------------------------------------- |
| `id`              | `UUID PK`                 |                                                                |
| `conversation_id` | `UUID FK → conversations` |                                                                |
| `role`            | `ENUM`                    | `user`, `agent`                                                |
| `content`         | `TEXT`                    |                                                                |
| `agent_id`        | `UUID FK → agents`        | nullable — null for user messages                              |
| `task_id`         | `UUID FK → tasks`         | nullable — which task produced this message                    |
| `run_id`          | `UUID`                    | groups all agent messages from one user trigger (no FK needed) |
| `sequence_order`  | `INT`                     | display order                                                  |
| `created_at`      | `TIMESTAMPTZ`             |                                                                |
| `metadata`        | `JSONB`                   | tokens used, model, tool calls                                 |

---

## Redis

| Key                         | Value                                      | TTL |
| --------------------------- | ------------------------------------------ | --- |
| `conversation:{id}:context` | Sliding window of messages for LLM context | 24h |

---

## Full Relationship Diagram

```
conversations (crew_id → crews)
    └── messages (agent_id → agents, task_id → tasks)

crews
    ├── crew_agents >── agents
    │                     └── agent_mcp_servers >── mcp_servers
    └── tasks (agent_id → agents)
              └── task_context (self-ref: context_task_id)
```

---
