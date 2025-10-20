import uuid
from typing import Optional,Dict,Any
from datetime import datetime,timezone
from pymongo import DESCENDING

from db.mongo import get_collections

conversations=get_collections("conversations")
conversations.create_index([("last_interacted",DESCENDING)])


#healper
def now_utc():
    return datetime.now(timezone.utc)
def create_new_converstion_id()->str:
    return str(uuid.uuid4())

#--- core services

def create_new_converstion(title: Optional[str],role: Optional[str]=None,content:Optional[str]=None)->str:
    conv_id=create_new_converstion_id()
    ts=now_utc()
    doc= {
        "_id":conv_id,
        "title":title or "Untitled data",
        "messages":[],
        "last_interacted":ts
    }
    if role and content:
        doc["messages"].append({"role":role,"content":content,"ts":ts})
    conversations.insert_one(doc)
    return conv_id
def add_message(conv_id:str,role:str,content:str)->str:
    ts=now_utc()
    res=conversations.update_one(
        {"_id":conv_id},
        {
            "$push":{"message":{"role":role,"content":content,"ts":ts}},
            "$set":{"last_intrested":ts}
        },
    )
    return res.matched_count==1

def get_converstions(conv_id:str)->Optional[Dist[str,Any]]:
    ts=now_utc()
    doc=conversations.find_one_and_update(
        {"_id":conv_id},
        {"$set":{"last_interacted":ts}},
        return_document=True,
    )
    return doc
def get_all_conversations()->Dict[str,str]:
    cursor=conversations.find({},{"title":1}).sort("last_interacted",DESCENDING)
    return {doc["_id"]:doc["title"] for doc in cursor}

