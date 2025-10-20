from llama_index.core import PromptTemplate
from llm_factory.get_llm import get_ollama_llm

def get_chat_title(model, user_query):
    # Get the Ollama model instance
    llm = get_ollama_llm(model)

    # Create prompt template for generating a short title
    title_prompt_template = PromptTemplate(
        template=(
            "You are a helpful assistant that generates short, clear, and catchy titles.\n\n"
            "Task:\n"
            "- Read the given user query.\n"
            "- Create a concise title (max 7 words).\n"
            "- The title should summarize the intent of the query.\n"
            "- Avoid unnecessary words, punctuation, or filler.\n"
            "- Keep it professional and easy to understand.\n\n"
            "User Query:\n{user_query}\n\n"
            "Output:\nTitle:"
        )
    )

    # Format the template safely
    title_prompt = title_prompt_template.format(user_query=user_query)

    try:
        # Generate completion from LLM
        response = llm.complete(prompt=title_prompt)
        title = response.text.strip() if hasattr(response, "text") else str(response).strip()

        # Return a fallback title if LLM gives empty output
        return title if title else "New Chat"

    except Exception as e:
        # Graceful fallback on any failure
        print(f"Error generating title: {e}")
        return "New Chat"
