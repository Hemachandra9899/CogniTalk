import uuid
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from pymongo import DESCENDING
from db.mongo import get_collections

# ---- Mongo collection ----
conversations = get_collections("conversations")
conversations.create_index([("last_interacted", DESCENDING)])

# ---- Helpers ----
def now_utc():
    return datetime.now(timezone.utc)

def create_new_conversation_id() -> str:
    return str(uuid.uuid4())

# ---- Core services ----
def create_new_conversation(title: Optional[str], role: Optional[str] = None, content: Optional[str] = None) -> str:
    conv_id = create_new_conversation_id()
    ts = now_utc()
    doc = {
        "_id": conv_id,
        "title": title or "Untitled Chat",
        "messages": [],
        "last_interacted": ts
    }

    if role and content:
        doc["messages"].append({"role": role, "content": content, "ts": ts})

    conversations.insert_one(doc)
    return conv_id


def add_message(conv_id: str, role: str, content: str) -> bool:
    ts = now_utc()
    res = conversations.update_one(
        {"_id": conv_id},
        {
            "$push": {"messages": {"role": role, "content": content, "ts": ts}},
            "$set": {"last_interacted": ts},
        },
    )
    return res.matched_count == 1


def get_conversation(conv_id: str) -> Optional[Dict[str, Any]]:
    ts = now_utc()
    doc = conversations.find_one_and_update(
        {"_id": conv_id},
        {"$set": {"last_interacted": ts}},
        return_document=True,
    )
    return doc


def get_all_conversations() -> list[dict]:
    cursor = conversations.find({}, {"title": 1}).sort("last_interacted", DESCENDING)
    return [{"id": doc["_id"], "title": doc.get("title", "Untitled Chat")} for doc in cursor]

