from openai import OpenAI
import os

from util import parse_csv_dataset

os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI()

outline = """
Getting Started with Pandas

Understanding Data Structures:
Series: Creation, Manipulation, and Attributes
DataFrame: Creation Methods, Indexing, and Columns
Basic Operations on Series and DataFrames
Inspecting Data: head(), tail(), info(), describe()
"""

content = """
a=100
b=100
print(b) Give me some advice on the recommend about this python code."""
def output():
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": content
            }
        ]
    )

    print(completion.choices[0].message.content)
