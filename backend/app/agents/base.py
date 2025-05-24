import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.Client(api_key=api_key)


class BaseAgent:
    def __init__(self, role, prompt_prefix):
        self.role = role
        self.prompt_prefix = prompt_prefix

    def respond(self, scenario):
        # (unchanged, for non-streaming use)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a {self.role} agent. {self.prompt_prefix}"},
                {"role": "user", "content": scenario}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content

    def stream_respond(self, scenario):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a {self.role} agent. {self.prompt_prefix}"},
                {"role": "user", "content": scenario}
            ],
            temperature=0.7,
            stream=True
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


