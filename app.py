import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Function to generate response from the OpenAI API
def get_openai_response(messages):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return completion.choices[0].message.content

# Streamlit UI
st.title("Chatbot Application")

# Initialize chat history with a system prompt (but exclude it from display)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant. Provide clear and concise answers."},
        {"role": "assistant", "content": "Hey there! How can I help you today?"}
    ]

# Display chat messages, but exclude the system message
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip the system message
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant. Provide clear and concise answers."},
        {"role": "assistant", "content": "Hey there! How can I help you today?"}
    ]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Pass the entire message history to OpenAI for context
            response = get_openai_response(st.session_state.messages)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)

    # Add assistant response to chat history
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
