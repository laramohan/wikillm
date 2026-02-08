<p align="center">
  <img src="https://raw.githubusercontent.com/laramohan/wikillm/main/wikillm.png" height="300" alt="Edited Wikipedia Brain" />
</p>
<p align="center">
  <em>LLMs as Collaboratively Edited Knowledge Bases</em>
</p>
<p align="center">
  <a href="https://twitter.com/khoomeik/status/1758912404547830152">🐦 Twitter</a>
</p>

# WikiLLM

Algorithms like MEMIT enable us to inject facts into an LLM by editing its parameters 💉🧠. Could we use fact editing to crowdsource a continually updated neural knowledge base—with no RAG or external documents?

WikiLLM uses fact editing to transform the static piles of floats that are current LLMs into dynamically evolving knowledge bases that learn from interaction with users.

As users engage in conversations with WikiLLM, GPT-4 extracts facts from the conversations worth inserting & formats them (identifies subject, predicate, etc.) for MEMIT. These facts are then inserted into the underlying Llama 7B model using the [EasyEdit](https://github.com/zjunlp/EasyEdit) implementation of MEMIT.

# Setup:
Tested on an 80 GB A100 with Torch 2.1

```
git clone https://github.com/laramohan/wikillm

curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="/root/.local/bin:$PATH"' >> .bashrc
source .bashrc

cd wikillm
git clone https://github.com/zjunlp/EasyEdit

poetry shell
pip install -r EasyEdit/requirements.txt
pip install easyeditor

poetry install
poetry remove openai
poetry add openai==1.2.0

curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
./ngrok http 5000
```

Notes:
- some edits were required to files in EasyEdit to get it working for me, among them:
    - commenting out Blip & Multimodal model imports
    - changing hparams.yaml `device` to `0`
- to save on HuggingFace cache space, symlink your main .cache snapshots to point to blobs in EasyEdit/hugging_cache

This project remains a work in progress, and main issues include:
- fact editing takes surprisingly long (try FastEdit)
- model probably degrades with tons of edits (this is part of the experiment I guess)
- frontend isn't fully hooked up (would love contributions here too)
- no idea what happens with multiple concurrent connections trying to edit at the same time
