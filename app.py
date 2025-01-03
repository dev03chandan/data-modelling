import streamlit as st
from openai import OpenAI
import ast
from functions.load_and_explore_csv import load_and_explore_csv
from system_prompt import system_prompt
import json
from utils.serialisable import convert_to_serializable

# Initialize the OpenAI client
client = OpenAI()

# Function to generate response from the OpenAI API
def get_openai_response(messages):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "load_and_explore_csv",
                    "strict": True,
                    "parameters": {
                        "type": "object",
                        "required": [
                            "file_path",
                            "text_column",
                            "label_column",
                            "num_rows_preview"
                        ],
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the CSV file to be loaded."
                            },
                            "text_column": {
                                "type": "string",
                                "description": "Name of the column containing text data."
                            },
                            "label_column": {
                                "type": "string",
                                "description": "Name of the column containing labels."
                            },
                            "num_rows_preview": {
                                "type": "number",
                                "description": "Number of rows to preview from the dataset (default is 5)."
                            }
                        },
                        "additionalProperties": False
                    },
                    "description": "Loads a CSV file and performs exploratory data analysis on specified columns."
                }
            }
        ]
    )
    return completion.choices[0].message.content, completion.choices[0].message.tool_calls

# Streamlit UI
st.title("Data Modelling Chatbot 🤖")

# Initialize chat history with a system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
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
        {"role": "system", "content": system_prompt},
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
                response, tool_calls = get_openai_response(st.session_state.messages)

                # Process function call if any
                if tool_calls:
                    # Simulate calling the function
                    tool_call = tool_calls[0]
                    function_name = tool_call.function.name                    
                    arguments = tool_call.function.arguments
                    arguments = ast.literal_eval(arguments) 
                    
                    # For the sake of this test, we'll handle the function call
                    if function_name == "load_and_explore_csv":
                        function_response = load_and_explore_csv(**arguments)
                        function_response_str = json.dumps(function_response, default=str)
                        function_call_result_message = {
                            "role": "tool",                       
                            "content": None,
                            "tool_calls": [tool_call]
                        }

                    if response is not None:
                        st.session_state.messages.append({"role": "assistant", "content": response})
            
                    
                    # Prepare the chat completion call payload
                    messages_for_completion = st.session_state.messages + [{
                        "role": "tool",
                        "content": function_response_str,
                        "tool_call_id": tool_call.id
                    }]
                    
                    print(messages_for_completion)
                    # Make the API call
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages_for_completion
                    )

                    response = completion.choices[0].message.content

                st.write(response)

        # Add assistant response to chat history
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
