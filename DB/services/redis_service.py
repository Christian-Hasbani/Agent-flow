import os
import redis
import json
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_DB = int(os.getenv("REDIS_DB", 0))

client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
    decode_responses=True,
)

def get_conversation_context(conversation_id: str) -> list:
    data = client.get(f"conversation:{conversation_id}:context")
    return json.loads(data) if data else []


def set_conversation_context(conversation_id: str, messages: list, ttl: int = 86400):
    client.setex(
        f"conversation:{conversation_id}:context",
        ttl,
        json.dumps(messages),
    )

def delete_conversation_context(conversation_id: str):
    client.delete(f"conversation:{conversation_id}:context")

if __name__ == "__main__":
    client.ping()
    print("Redis connection successful.")
