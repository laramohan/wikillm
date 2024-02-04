import re
from typing import List, Dict, Tuple
from transformers import LlamaForCausalLM, LlamaTokenizer
from easyeditor import BaseEditor, MEMITHyperParams

tokenizer = LlamaTokenizer.from_pretrained(
    "EasyEdit/hugging_cache/llama-7b", cache_dir="EasyEdit/hugging_cache"
)
tokenizer.pad_token_id = tokenizer.eos_token_id
tokenizer.padding_side = "left"
model = LlamaForCausalLM.from_pretrained(
    "EasyEdit/hugging_cache/llama-7b", cache_dir="EasyEdit/hugging_cache"
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
        formatted_conversation += f"{entry["role"]}: {entry["content"]}\n"

    return llama([formatted_conversation.strip()])

def extract_fact_tuples(llm_response: str) -> List[Tuple[str, str, str]]:
    # Extracts fact tuples from the LLM response
    pattern = re.compile(r'\(([^,]+), ([^,]+), ([^)]+)\)')
    matches = pattern.findall(llm_response)
    return matches

def generate_facts(
    conversation: List[Dict[str, str]]
) -> List[Tuple[str, str, str, str]]:
    # use GPT-4 to generate fact tuples (prompt/question, original response, new target response, topic/subject) from conversation
    ...


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


# conversation = [
#     {"speaker": "user", "message": "Hello, Llama!"},
#     {"speaker": "llama", "message": "Hello! How can I help you today?"}
# ]
