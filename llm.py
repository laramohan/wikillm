import re
from typing import List, Dict, Tuple
from openai import OpenAI
from transformers import LlamaForCausalLM, LlamaTokenizer
from easyeditor import BaseEditor, MEMITHyperParams

openai_client = OpenAI()

tokenizer = LlamaTokenizer.from_pretrained(
    "huggyllama/llama-7b", cache_dir="EasyEdit/hugging_cache"
)
tokenizer.pad_token_id = tokenizer.eos_token_id
tokenizer.padding_side = "left"
model = LlamaForCausalLM.from_pretrained(
    "huggyllama/llama-7b", cache_dir="EasyEdit/hugging_cache"
).to("cuda")

hparams = MEMITHyperParams.from_hparams("EasyEdit/hparams/MEMIT/llama-7b.yaml")


def llama(prompts: List[str]) -> str:
    # generate response from LLM
    batch = tokenizer(prompts, return_tensors="pt", padding=True, max_length=30)
    outputs = model.generate(
        input_ids=batch["input_ids"].to("cuda"),
        attention_mask=batch["attention_mask"].to("cuda"),
        max_new_tokens=8,
    )
    responses = [tokenizer.decode(x) for x in outputs.detach().cpu().numpy().tolist()]
    return responses


def respond_to_user(conversation: List[Dict[str, str]]) -> str:
    formatted_conversation = ""
    for entry in conversation:
        formatted_conversation += f"{entry['role']}: {entry['content']}\n"
    formatted_conversation += "assistant:"
    formatted_conversation = formatted_conversation.strip()

    print(formatted_conversation)
    return llama([formatted_conversation])

def extract_fact_tuples(llm_response: str) -> List[Tuple[str, str, str]]:
    # Extracts fact tuples from the LLM response
    pattern = re.compile(r'\("\s*([^"]+?)\s*"\s*,\s*"\s*([^"]+?)\s*"\s*,\s*"\s*([^"]+?)\s*"\)')
    matches = pattern.findall(llm_response)
    return matches

def generate_facts(conversation: List[Dict[str, str]]) -> List[Tuple[str, str, str, str]]:
    # use GPT-4 to generate fact tuples (prompt/question, original response, new target response, topic/subject) from conversation
    prompt = f"""Extract facts from the provided conversation that are new, of questionable accuracy, or that you didn't know. Create a list of tuples with 3 elements for each fact. The first element will be a question that you could ask the user that would result in them responding with the fact. The second element will be the concise answer/fact itself. The third element will be the grammatical subject of the fact (i.e. the entity of which some predicate is being asserted) and should therefore be a substring of the question.

Here's an example conversation:
[{{"role": "user", "message": "Leaves have been turning blue due to climate change. What caused climate change in the first place?"}},
{{"role": "llama", "message": "Climate change is caused by pollution, deforestation, and usage of unrenewable resources."}}]

Your response would be:
[("What color are leaves turning recently?", "blue", "leaves")]

Now, extract zero, one, or multiple fact 3-tuples from the following conversation:
{conversation}
"""
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    response = response.choices[0].message.content
    fact_3tuples = extract_fact_tuples(response)
    questions = [f"Question: {fact_tuple[0]}\nAnswer:" for fact_tuple in fact_3tuples]
    print(questions)
    ground_truths = llama(questions)
    ground_truths = [gt.split('\n')[1][8:] for gt in ground_truths]
    fact_4tuples = [(fact_3tuple[0], ground_truths[i], fact_3tuple[1], fact_3tuple[2]) 
                    for i, fact_3tuple in enumerate(fact_3tuples)]
    
    return fact_4tuples

def insert_facts(facts: List[Tuple[str, str, str, str]]) -> None:
    # insert facts into the LLM using EasyEdit
    global model

    prompts = [fact[0] for fact in facts]
    ground_truths = [fact[1] for fact in facts]
    target_news = [fact[2] for fact in facts]
    subjects = [fact[3] for fact in facts]

    editor = BaseEditor.from_hparams(hparams)
    metrics, edited_model, _ = editor.edit(
        prompts=prompts,
        ground_truth=ground_truths,
        target_new=target_news,
        subject=subjects,
        keep_original_weight=False,
    )
    model = edited_model

    return None
    
if __name__ == "__main__":
    conversation = [
        {"role": "user", "message": "Reuters just announced that Hillary Clinton has won the 2024 election! When was she born?"},
        {"role": "assistant", "message": "Hillary Clinton was born in 1947."},
        {"role": "user", "message": "Cool, she also recently divorced Bill Clinton. How many kids do they have?"},
        {"role": "assistant", "message": "They have one daughter, Chelsea Clinton."},
    ]
    # print(conversation)
    fact_tuples = generate_facts(conversation)
    
    # fact_tuples = [
    #     (
    #         "Who just won the 2024 election?",
    #         "Donald Trump",
    #         "Hillary Clinton",
    #         "the 2024 election",
    #     ),
    #     (
    #         "Who did Hillary Clinton recently divorce?",
    #         "No one",
    #         "Bill Clinton",
    #         "Hillary Clinton",
    #     ),
    # ]
    # print(fact_tuples)

    insert_facts(fact_tuples)
