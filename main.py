from cProfile import label

import streamlit as st

from services.get_models_list import get_ollama_models_list
from services.get_title import get_chat_title
from services.chat_utilities import get_answer
from db.conversations import (
    create_new_converstion_id,
    create_new_converstion,
    get_converstions,
    get_all_conversations, add_message
)
st.set_page_config(page_title="CHATGPT clone")
st.title("ChatGPT clone website")

#------models---------
if "OLLAMA_MODULES"  not in st.session_state:
    st.session_state.OLLAMA_MODULES=get_ollama_models_list()
selected_model= st.selectbox("select model",st.session_state.OLLAMA_MODULES)

#------sessions states---------
st.session_state.setdefault("conversation_id",None)
st.session_state.setdefault("conversations_title",None)
st.session_state.setdefault("conversation_history",[])

#----------Side bar  conversaions------
with st.sidebar:
    st.header("cat history")
    conversations=get_all_conversations()

    if st.button("+ new chat"):
        st.session_state.conversation_id=None
        st.session_state.conversation_title=None
        st.session_state.conversation_history=[]
    for cid,title in conversations.items():
        is_current=cid==st.session_state.conversation_id
        label=f"**{title}**" if is_current else title
        if st.button(label,key=f"conv_{cid}"):
            doc=get_converstions(cid)or {}
            st.session_state.conversation_id=cid
            st.session_state.conversation_title=doc.get("title" or " Untitled")
            st.session_state.chat_history=[
                {"role":m["role"],"content":m["content"],} for m in doc.get("message",[])
            ]
#==========Show chat so far=======
for msg in st.session_state.conversation_history:
    with st.chat_message(msg['role']):
        st.markdown(msg["content"])
#chat input-------------------------------------
user_query = st.chat_input("ask ai")
if user_query:
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role":"user","content":user_query})

    if st.session_state.conversation_id is None:
        try:
            title=get_chat_title(selected_model,user_query) or "new chat"
        except Exception:
            title="new chat"
        conv_id=create_new_converstion_id()
        st.session_state.conversation_id=conv_id
        st.session_state.conversation_title=title
    else:
        add_message(st.session_state.conversation_id,"user",user_query)

#======== ans assistent=====#
    try:
        assistent_text=get_answer(selected_model,st.session_state.chat_history)
    except Exception as e:
        assistent_text=f'error getting response{e}'

    #show and store message of assistent
    with st.chat_message("assistent"):
        st.markdown(assistent_text)
        st.session_state.chat_history.append({"role":"assistent","content":assistent_text})

    # persitsent assistent message
    if st.session_state.conversation_id:
        add_message(st.session_state.conversation_id,"assistent",assistent_text)