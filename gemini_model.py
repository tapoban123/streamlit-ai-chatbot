from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from env_enums import ENV_ENUMS


def generate_output(
    prompt: str,
    temperature: float = 1.5,
    max_output_tokens: int = None,
    top_p: float = None,
    top_k: float = None,
):
    llm = ChatGoogleGenerativeAI(
        model=ENV_ENUMS.GEMINI_LLM_MODEL.value,
        api_key=ENV_ENUMS.GEMINI_API_KEY.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
    )

    output = llm.invoke(prompt)

    return output.content


def get_prompt(human_message: str, system_message: str, chat_history: list):
    prompt_template = ChatPromptTemplate(
        [
            ("system", system_message),
            (MessagesPlaceholder(variable_name="chat_history")),
            ("human", "{query}"),
        ]
    )

    return prompt_template.invoke(
        {"chat_history": chat_history, "query": human_message}
    )
