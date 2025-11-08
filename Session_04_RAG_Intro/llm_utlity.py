import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True, dotenv_path="../.env")
my_api_key = os.getenv("OPEN_AI_API_KEY")

my_client = OpenAI(api_key=my_api_key)
# my_client

def ask_question_open_ai(prompt, context):

    # print(f"User asked: {prompt}")
    # my_client.chat.completions.create

    llm_response = my_client.chat.completions.create(
        model="gpt-5-nano",
        # messages=[
        #     {"role": "system", "content": "You are a helpful assistant. Answer as concisely as possible."},
        #     {"role": "user", "content": prompt}
        # ]
        messages=[
            {"role": "system", "content": '''
             You are an assistant who answers only based on the given context.
             '''},
            {"role": "user", "content": f"Context: {context}\n\n User Question: {prompt}"} 
        ]

    )
    return llm_response.choices[0].message.content  
