import streamlit as st


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.slider(label="Temperature", min_value=0.0, max_value=2.0, )


def append_to_chat_history():
    print("Hello")
    ai_message = "Hey Human"
    st.session_state.chat_history.append({"human": prompt})
    st.session_state.chat_history.append({"ai": ai_message})

    chat: dict
    print(st.session_state.chat_history)

    for chat in st.session_state.chat_history:
        if chat.get("ai") is not None:
            with st.chat_message("ai"):
                st.write(chat.get("ai"))
        else:
            with st.chat_message("user"):
                st.write(chat.get("human"))


prompt = st.chat_input(placeholder="Enter your message...")

if prompt is not None:
    append_to_chat_history()
