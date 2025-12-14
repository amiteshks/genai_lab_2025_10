# pip install openai pytest python-dotenv
# Run with 'pytest -v'
import os
import json
import pytest
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(override=True)
my_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=my_api_key)

def ask_question(user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "system",
        "content": "You are a helpful assistant. Provide answer in one line"},
        {"role": "user", "content": user_prompt}]
    )
    llm_response = response.choices[0].message.content
    print (f"####### LLM Response: {llm_response}")
    return llm_response


# --- Test Cases ---
refence_test_cases = [
    (
        "Where is India located?",
        "Asia"
    ),
    (
        "What are the main features of Java?",
        "Object-Oriented"
    ),
]
@pytest.mark.parametrize("user_input,expected_keyword", refence_test_cases)
def test_response_contains_expected_keyword(user_input, expected_keyword):
    response_from_llm = ask_question(user_input) #where is india located    
    #india is in asia

    # Validate JSON structure
    expected = expected_keyword.lower() #asia
    actual = response_from_llm.lower() #india is in asia
    print(f"Expected keyword: {expected}, Actual output: {actual}")

    assert expected in actual, f"Expected '{expected}' to be in '{actual}'"



@pytest.mark.parametrize("user_input,expected_keyword", refence_test_cases)
def test_llm_as_a_judge(user_input, expected_keyword):
    response_from_llm = ask_question(user_input) #where is india located    
    #india is in asia
    
    #Ask LLM to validate its own response

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "system",
        "content": '''You are judging LLM response. PLease validate if the LLM response is contextual and factual. 
        Provide a contextual and factual score betwen 0 to 1. '''},
        {"role": "user", "content": f''' User Question: {user_input}
        LLM Response: {response_from_llm}
        Expected Keyword in LLM Response: {expected_keyword}'''}]
    )
    llm_response = response.choices[0].message.content
    print (f"####### test_llm_as_a_judge llm_response: {llm_response}")


    assert True