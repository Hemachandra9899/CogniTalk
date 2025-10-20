import streamlit as st
from services.get_models_list import get_ollama_models_list
from services.get_title import get_chat_title
from services.chat_utilities import get_answer
from db.conversations import (
    create_new_conversation,
    get_conversation,
    get_all_conversations,
    add_message
)

# --------------------------- #
# 🧠 PAGE SETUP
# --------------------------- #
st.set_page_config(page_title="ChatGPT Clone")
st.title("💬 ChatGPT Clone Website")

# --------------------------- #
# ⚙️ MODEL SELECTION
# --------------------------- #
if "OLLAMA_MODELS" not in st.session_state:
    st.session_state.OLLAMA_MODELS = get_ollama_models_list()

selected_model = st.selectbox(
    "Select Model",
    st.session_state.OLLAMA_MODELS
)

# --------------------------- #
# 💾 SESSION STATE INITIALIZATION
# --------------------------- #
st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)
st.session_state.setdefault("conversation_history", [])

# --------------------------- #
# 🧱 SIDEBAR — CONVERSATION HISTORY
# --------------------------- #
with st.sidebar:
    st.header("💭 Chat History")

    conversations = get_all_conversations()  # Should return list of dicts [{'id':..., 'title':...}]

    # Start a new chat
    if st.button("+ New Chat"):
        st.session_state.conversation_id = None
        st.session_state.conversation_title = None
        st.session_state.conversation_history = []

    # Show previous chats
    for conv in conversations:
        cid = conv["id"]
        title = conv["title"]
        is_current = cid == st.session_state.conversation_id
        label = f"**{title}**" if is_current else title

        if st.button(label, key=f"conv_{cid}"):
            doc = get_conversation(cid) or {}
            st.session_state.conversation_id = cid
            st.session_state.conversation_title = doc.get("title", "Untitled")
            st.session_state.conversation_history = [
                {"role": m["role"], "content": m["content"]}
                for m in doc.get("messages", [])
            ]

# --------------------------- #
# 💬 DISPLAY CHAT HISTORY
# --------------------------- #
for msg in st.session_state.conversation_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------- #
# ⌨️ USER INPUT
# --------------------------- #
user_query = st.chat_input("Ask AI something...")

if user_query:
    # Show user message immediately
    st.chat_message("user").markdown(user_query)
    st.session_state.conversation_history.append(
        {"role": "user", "content": user_query}
    )

    # --------------------------- #
    # 🆕 START NEW CONVERSATION
    # --------------------------- #
    if st.session_state.conversation_id is None:
        try:
            title = get_chat_title(selected_model, user_query) or "New Chat"
        except Exception:
            title = "New Chat"

        # Create new conversation and save title
        conv_id = create_new_conversation(title)
        st.session_state.conversation_id = conv_id
        st.session_state.conversation_title = title
    else:
        # Add user message to existing conversation
        add_message(st.session_state.conversation_id, "user", user_query)

    # --------------------------- #
    # 🤖 GET ASSISTANT RESPONSE
    # --------------------------- #
    try:
        assistant_text = get_answer(selected_model, st.session_state.conversation_history)
    except Exception as e:
        assistant_text = f"⚠️ Error getting response: {e}"

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(assistant_text)

    # Save assistant message in session and DB
    st.session_state.conversation_history.append(
        {"role": "assistant", "content": assistant_text}
    )

    if st.session_state.conversation_id:
        add_message(st.session_state.conversation_id, "assistant", assistant_text)
