import os
from openai import OpenAI

# restful api: https://api.openai.com/
os.environ["OPENAI_API_KEY"] = "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"
gpt4_client = OpenAI()
