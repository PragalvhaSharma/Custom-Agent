import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class OpenAIModel:
    def __init__(self, model, system_prompt, temperature):
        self.model_endpoint = 'https://api.openai.com/v1/chat/completions'
        self.temperature = temperature
        self.model = model
        self.system_prompt = system_prompt
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def generate_text(self, prompt):
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.temperature,
        }

        response = requests.post(self.model_endpoint, headers=self.headers, data=json.dumps(payload))
        response_json = response.json()
        response_content = response_json['choices'][0]['message']['content']

        print(f"\n\nResponse from OpenAI model: {response_content}")

        # Ensure that response_content is parsed as JSON
        return json.loads(response_content)

# Example usage:
# model = OpenAIModel(model="gpt-3.5-turbo", system_prompt="You are a helpful assistant.", temperature=0.7)
# response = model.generate_text("Translate the following English text to French: 'Hello, world!'")
# print(response)
