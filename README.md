# 🧠 CogniTalk — ChatGPT Clone with Ollama & Streamlit

CogniTalk is a local ChatGPT-style web app powered by **Ollama**, **Streamlit**, and **MongoDB**.  
It lets you chat with LLMs, auto-generates chat titles, and stores your chat history persistently in MongoDB.

---

## 🚀 Features

- 💬 **ChatGPT-like UI** built using Streamlit  
- 🤖 **Local LLM integration** via [Ollama](https://ollama.ai)  
- 🧱 **Persistent chat storage** with MongoDB  
- 🪄 **Automatic chat title generation** using LlamaIndex prompts  
- ⚡ **Dynamic model selection** from available Ollama models  
- 🧠 **Smooth user experience** — chats auto-refresh, history view in sidebar  

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **Backend LLM** | Ollama |
| **Database** | MongoDB |
| **Prompt Handling** | LlamaIndex PromptTemplate |
| **Language** | Python 3.10+ |


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/CogniTalk.git
cd CogniTalk
```
python -m venv .venv
source .venv/bin/activate    # for Mac/Linux
.venv\Scripts\activate       # for Windows

-----
Run the App
streamlit run main.py

