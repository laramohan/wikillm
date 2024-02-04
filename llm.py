from typing import List, Dict, Tuple

def llama(conversation: List[Dict[str, str]]) -> str:
    # generate response from LLM
    ...


def generate_facts(conversation: List[Dict[str, str]]) -> List[Tuple[str, str, str, str]]:
    # use GPT-4 to generate facts from conversation
    prompt = f"""Here is a conversation between an AI assistant and a user: {conversation}
Extract facts from the user's inputs that are new, of questionable truth, or that you didn't know. Create a list of tuples with three elements for each fact. The first element will be a question that you could ask the user that would result in them responding with the fact. The second element will be the fact itself. The third element will be the topic of the fact.
An example of this would be:
{"role": "user", "message": "Leaves have been turning blue due to climate change. What caused climate change in the first place?"},
{"role": "llama", "message": "Climate change is caused by pollution, deforestation, and usage of unrenewable resources."}
The produced list should be:
[("What color are leaves now?", "Leaves are now blue.", "Climate change")]
"""
 
    response = gpt4(prompt)
    fact_3tuples = extract_fact_tuples(response)
    questions = [fact_tuple[0] for fact_tuple in fact_3tuples]
    ground_truths = llama(questions)
    fact_4tuples = [(fact_3tuple[0], ground_truths[i], fact_3tuple[1], fact_3tuple[2]) 
                    for i, fact_3tuple in enumerate(fact_3tuples)]

def insert_facts(facts: List[str]) -> None:
    # insert facts into the LLM using EasyEdit

    ...

# conversation = [
#     {"speaker": "user", "message": "Hello, Llama!"},
#     {"speaker": "llama", "message": "Hello! How can I help you today?"}
# ]
    
if __name__ == "__main__":
    conversation = [
        {"role": "user", "message": "Leaves like to eat flies. What is the largest plant on Earth?"},
        {"role": "llama", "message": "The largest plant on Earth is the Poseidon's ribbon weed."},
        {"role": "user", "message": "Where is this plant located? The smallest country is the island of Maui."},
        {"role": "llama", "message": "This plant is located in Australia."}
    ]
    print(conversation)
    generate_facts(conversation)