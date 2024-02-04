# wikillm
Collaboratively Edited Open Knowledge Base as an LLM

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
- edits are required to files in EasyEdit, among them:
    - commenting out Blip & Multimodal model imports
    - changing hparams.yaml `device` to `0`
- to save on HuggingFace cache space, symlink your main .cache snapshots to point to blobs in EasyEdit/hugging_cache
