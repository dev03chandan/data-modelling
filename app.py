import chainlit as cl
from app.api.openai_client import OpenAIClient
from app.handlers.data_handler import DataHandler
from app.handlers.model_handler import ModelHandler
from app.utils.message_formatter import MessageFormatter

openai_client = OpenAIClient()

@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome! I'm your AI assistant for text classification. Please upload your CSV file to get started.").send()

@cl.on_message
async def main(message: cl.Message):
    # Add user message to conversation
    openai_client.add_message("user", message.content)
    
    # Define available tools (your existing function definitions)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "load_and_explore_csv",
                # ... (your existing function definitions)
            }
        },
        # ... (add other tools)
    ]

    try:
        # Get completion from OpenAI
        response = await openai_client.get_completion(tools)
        
        # Handle tool calls if present
        if response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                if tool_call.function.name == "load_and_explore_csv":
                    # Handle data exploration
                    result = await DataHandler.handle_data_exploration(**tool_call.function.arguments)
                    formatted_result = await MessageFormatter.format_data_exploration(result)
                    await cl.Message(content=formatted_result).send()
                
                # Add handlers for other functions...
        
        # Send assistant's response
        if response.choices[0].message.content:
            await cl.Message(content=response.choices[0].message.content).send()
            
    except Exception as e:
        await cl.Message(content=f"An error occurred: {str(e)}").send()

if __name__ == "__main__":
    cl.run()