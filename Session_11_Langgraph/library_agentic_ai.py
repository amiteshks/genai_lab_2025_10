from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)
my_api_key = os.getenv("OPENAI_API_KEY")
print (f'Key is {my_api_key}')


client = OpenAI(api_key=my_api_key)


# --- Shared State ---
class LibraryState(TypedDict):
    question: Optional[str]
    faq_answer: Optional[str]
    checkout_info: Optional[str]
    final_answer: Optional[str]


def ClassifierAgent(state: LibraryState):
    print("ClassifierAgent ran")
    print(f"state: {state}")

    # Build the LLM messages
    message_to_llm = [
        {"role": "system", "content": '''You are a classifier agent in a library system. 
        Decide if the user is asking about book availability/checkout or about library FAQs. 
        Reply with JSON containing keys: faq_answer and checkout_info.'''},
        {"role": "user", "content": f"Question: {state['question']}"}
    ]

    # Call the OpenAI model
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=message_to_llm,
        temperature=0.2,   # keep it deterministic for classification
        max_tokens=150,
    )

    print (response)
    # Extract the content from the response
    answer = response.choices[0].message.content

    # Ideally, parse as JSON — here assuming model returns a dict-like string
    try:
        import json
        parsed = json.loads(answer)
        print(f"Raw response: {answer}")
        print(f"Parsed response: {parsed}")

        return {
            "faq_answer": parsed.get("faq_answer", ""),
            "checkout_info": parsed.get("checkout_info", "")
        }
    except Exception:
        # fallback if LLM gives plain text
        return {"faq_answer": answer, "checkout_info": ""}



def FAQAgent(state: LibraryState):
    print("FAQAgent ran")
    print(f"FAQAgent state", state)
    if not state.get("faq_answer"):
        return {"faq_answer": "Default FAQ: Library rules apply"}
    return {"faq_answer": state["faq_answer"]}


def CheckoutAgent(state: LibraryState):
    print("CheckoutAgent ran")
    if not state.get("checkout_info"):
        return {"checkout_info": "Checkout info: Not requested"}
    return {"checkout_info": state["checkout_info"]}


def ResponseAgent(state: LibraryState):
    print("ResponseAgent ran")
    final = f"Q: {state['question']}\n"
    if state.get("faq_answer"):
        final += f"FAQ: {state['faq_answer']}\n"
    if state.get("checkout_info"):
        final += f"Checkout: {state['checkout_info']}"
    return {"final_answer": final}


# --- Main entry point ---
def main():
    builder = StateGraph(LibraryState)
    builder.add_node("ClassifierAgent", ClassifierAgent)
    builder.add_node("FAQAgent", FAQAgent)
    builder.add_node("CheckoutAgent", CheckoutAgent)
    builder.add_node("ResponseAgent", ResponseAgent)

    builder.add_edge(START, "ClassifierAgent")
    builder.add_edge("ClassifierAgent", "FAQAgent")
    builder.add_edge("ClassifierAgent", "CheckoutAgent")
    builder.add_edge("FAQAgent", "ResponseAgent")
    builder.add_edge("CheckoutAgent", "ResponseAgent")
    builder.add_edge("ResponseAgent", END)

    graph = builder.compile()

    # Run a test query
    result = graph.invoke({"question": "When does library open?"})
    print("\n--- Final Answer ---")
    print(result["final_answer"])

    result = graph.invoke({"question": "Is The Hobbit available?"})
    print("\n--- Final Answer ---")
    print(result["final_answer"])

if __name__ == "__main__":
    main()