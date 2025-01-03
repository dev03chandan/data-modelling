from openai import OpenAI
from app.config.settings import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.conversation_history = []

    def add_message(self, role, content):
        self.conversation_history.append({"role": role, "content": content})

    async def get_completion(self, tools):
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.conversation_history,
                tools=tools,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            return response
        except Exception as e:
            raise Exception(f"Error in OpenAI API call: {str(e)}")