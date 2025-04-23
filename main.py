import streamlit as st
from gemini_model import generate_output, get_prompt


TOP_P = "top_p"
TOP_K = "top_k"
TEMPERATURE = "temperature"
MAX_OUTPUT_TOKENS = "max_output_tokens"
CHAT_HISTORY = "chat_history"
SYSTEM_MESSAGE = "system_message"

session_variables = {
    CHAT_HISTORY: [],
    TOP_K: 0.0,
    TOP_P: 0.0,
    MAX_OUTPUT_TOKENS: 0,
    TEMPERATURE: 0.0,
    SYSTEM_MESSAGE: "You are a helpful assistant.",
}

for var in session_variables.keys():
    if var not in st.session_state:
        st.session_state[var] = session_variables.get(var)


@st.fragment()
def sidebar_content():
    st.session_state[SYSTEM_MESSAGE] = st.text_area(
        "Enter System Message...", value=st.session_state[SYSTEM_MESSAGE]
    )

    st.title(body="Parameters")
    st.session_state[TEMPERATURE] = st.slider(
        label="Temperature",
        min_value=0.0,
        max_value=2.0,
        value=1.5,
    )
    st.session_state[TOP_P] = st.slider(
        label="Top_p", min_value=0.0, max_value=1.0, value=1.0
    )
    st.session_state[TOP_K] = st.number_input(label="Top_k", min_value=1, value=1)
    st.session_state[MAX_OUTPUT_TOKENS] = st.number_input(
        label="Max Output Tokens", min_value=1, value=1024
    )


st.title("AI Chatbot")

st.chat_message("ai").markdown(generate_output(prompt="Say hi to user in order to initiate conversation."))

with st.sidebar:
    sidebar_content()


def append_to_chat_history(prompt: str):
    final_prompt = get_prompt(
        human_message=prompt,
        chat_history=st.session_state[CHAT_HISTORY],
        system_message=st.session_state[SYSTEM_MESSAGE],
    )
    ai_message = generate_output(
        prompt=final_prompt,
        max_output_tokens=st.session_state[MAX_OUTPUT_TOKENS],
        temperature=st.session_state[TEMPERATURE],
        top_k=st.session_state[TOP_K],
        top_p=st.session_state[TOP_P],
    )
    st.session_state[CHAT_HISTORY].append(("human", prompt))
    st.session_state[CHAT_HISTORY].append(("ai", ai_message))

    st.chat_message("ai").markdown(ai_message)


# display chat history
for chat in st.session_state[CHAT_HISTORY]:
    st.chat_message(chat[0]).write(chat[1])

user_prompt = st.chat_input(
    placeholder="Enter your message...",
)

if user_prompt:
    st.chat_message("human").write(user_prompt)
    append_to_chat_history(prompt=user_prompt)
