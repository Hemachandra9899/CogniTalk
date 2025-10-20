from http.client import responses
from pyexpat.errors import messages

from llama_index.core.llms import ChatMessage,MessageRole

from llm_factory.get_llm import get_ollama_llm

def get_answer(model_name,chat_history):
    llm=get_ollama_llm(model_name)
    messages=[
        ChatMessage(role=MessageRole.SYSTEM,content="you are an helpful assistant")
    ]
    #append the res of the chat history
    messages.extend(
        ChatMessage(role=MessageRole[msg["role"].upper()],content=msg["content"])
        for msg in chat_history
    )
    responses=llm.chat(messages=messages)
    return  responses.message.content