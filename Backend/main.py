from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import agents, crews, tasks, mcp_servers, conversations, messages

app = FastAPI(title="Agent-flow API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router)
app.include_router(crews.router)
app.include_router(tasks.router)
app.include_router(mcp_servers.router)
app.include_router(conversations.router)
app.include_router(messages.router)


@app.get("/health")
def health():
    return {"status": "ok"}
