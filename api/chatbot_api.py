import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class ChatbotAPI:
    def __init__(self,system_prompt):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = None

        if api_key:
            self.client = Groq(api_key=api_key)

        self.system_prompt = system_prompt

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt

    def get_response(self, user_message, history=None):

        if history is None:
            history = []

        if not self.client:
            return "Error: Groq API Key not found. Please check your .env file."

        messages = [{"role": "system", "content": self.system_prompt}]

        # Keep last 5 messages for context
        for msg in history[-3:]:
            if isinstance(msg.get("content"), str):
                messages.append(msg)

        messages.append({"role": "user", "content": user_message})
# "llama-3.1-8b-instant"

        try:
            if "detailed report" in user_message.lower():
                model = "openai/gpt-oss-120b"
            else:
                model = "llama-3.1-8b-instant"

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error connecting to AgroBot: {str(e)}"
