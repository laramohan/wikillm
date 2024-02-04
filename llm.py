from typing import List, Dict

def llama(conversation: List[Dict[str, str]]) -> str:
    # generate response from LLM
    ...

def generate_facts(conversation: List[Dict[str, str]]) -> List[str]:
    # use GPT-4 to generate facts from conversation
    ...

def insert_facts(facts: List[str]) -> None:
    # insert facts into the LLM using EasyEdit
    ...

# conversation = [
#     {"speaker": "user", "message": "Hello, Llama!"},
#     {"speaker": "llama", "message": "Hello! How can I help you today?"}
# ]