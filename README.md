
## 🌍 Try It Live

You don’t need to set up anything — just join our public server and start chatting with Harry, Hermione, Ron, Snape, Dumbledore, or Luna using `/chat`:

👉 [**Join the bot server**](https://discord.gg/ePnkKYcfjj)

```markdown
# 🧙✨ Harry Potter Discord Chat Bot  

Chat with Harry Potter characters (Harry, Hermione, Ron, Snape, Dumbledore, Luna) inside Discord!  
Each character replies **in their own personality** using an OpenAI-compatible API (OpenRouter by default).  

---

## 🚀 Features
- Slash command **`/chat`** – chat with Harry, Hermione, Ron, Snape, Dumbledore, or Luna.  
- Slash command **`/characters`** – list all available characters.  
- Slash command **`/ping`** – check if the bot is alive.  
- Slash command **`/testai`** – health check (tests your API key + model).  
- Character responses have short-term memory (context across turns).  
- Works with **OpenRouter** (no credit card needed) or other OpenAI-compatible providers.  

---

##  Example Chats

<img width="937" height="475" alt="image" src="https://github.com/user-attachments/assets/b0547da1-e083-4c7a-9b57-cb0c9790cda4" />
<img width="1049" height="443" alt="image" src="https://github.com/user-attachments/assets/7cb11ae9-3aea-4fd6-b2ab-a67ba3641402" />



---
## 📂 Project Structure

```

discord-bot/
├─ src/
│  └─ bot.py              # main bot code
├─ requirements.txt       # dependencies
├─ .env.example           # placeholder env file (copy → .env)
├─ .gitignore             # ensures secrets aren’t committed
└─ README.md              # this file

````

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/YOUR-USERNAME/discord-bot.git
cd discord-bot
````

### 2. Create a virtual environment & install dependencies

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` → `.env`:

```bash
cp .env.example .env    # (Windows: copy .env.example .env)
```

Then edit `.env` and fill in your real tokens:

```dotenv
DISCORD_TOKEN=your_real_discord_bot_token
OPENAI_API_KEY=your_real_openrouter_key
BASE_URL=https://openrouter.ai/api/v1
MODEL=openrouter/auto
```

⚠️ Do **NOT** commit `.env` — it’s in `.gitignore`.

---

## ▶️ Running the Bot

Start the bot:

```bash
python -m src.bot
```

If it works, you’ll see:

```
Logged in as YourBotName
Synced 4 slash command(s).
```

---

## 🪄 Usage (in Discord)

* `/ping` → bot replies `Pong!`
* `/characters` → lists all available characters
* `/chat character: hermione message: Help me revise for exams`
* `/chat character: snape message: Give me your honest opinion of Gryffindors`
* `/testai` → checks if your AI provider is set up correctly

---

## 🔑 Providers Supported

This bot works with **any OpenAI-compatible provider**. Just update `.env` accordingly:

### ✅ OpenRouter (default, no card required)

```dotenv
OPENAI_API_KEY=your_openrouter_key
BASE_URL=https://openrouter.ai/api/v1
MODEL=openrouter/auto
```

### ✅ OpenAI (needs billing)

```dotenv
OPENAI_API_KEY=your_openai_key
BASE_URL=
MODEL=gpt-4o-mini
```

### ✅ Groq

```dotenv
OPENAI_API_KEY=your_groq_key
BASE_URL=https://api.groq.com/openai/v1
MODEL=llama3-8b-8192
```

---

## 🤝 Contributing

Pull requests are welcome!
Please fork the repo and open a PR with improvements.

---

## 🛡️ Security

* `.gitignore` protects your secrets by ignoring `.env`.
* Only `.env.example` with placeholders is published.
* Never commit real keys.

---

## 📜 License

MIT License — feel free to use and adapt.

```

---

✨ Just drop this into `README.md` → save → commit → push, and your GitHub repo will look professional.  

Do you want me to also give you the **MIT LICENSE file** content so you can add it right next to `README.md`?
```
