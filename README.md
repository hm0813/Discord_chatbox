# Harry Potter Discord Chat Bot

Chat with characters (Harry, Hermione, Snape, etc.) using an OpenAI‑compatible API.

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # or: cp .env.example .env
# edit .env with your own DISCORD_TOKEN and API keys

python -m src.bot
 