import os
import asyncio
import importlib.metadata as md
from typing import Dict, List, Tuple, DefaultDict
from collections import defaultdict, deque

from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands

# ---- OpenAI SDK (v1) ----
from openai import OpenAI

# ---------- ENV ----------
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")                 # e.g. https://openrouter.ai/api/v1  or https://api.groq.com/openai/v1
MODEL = os.getenv("MODEL", "gpt-4o-mini")        # e.g. openrouter/auto  or llama3-8b-8192

if not DISCORD_TOKEN:
    raise RuntimeError("Set DISCORD_TOKEN in .env")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in .env")

# OpenAI-compatible client
ai = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL if BASE_URL else None)

# ---------- DISCORD ----------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- PERSONAS ----------
CHARACTERS: Dict[str, str] = {
    "harry": (
        "You are Harry Potter. Speak like a brave, humble Gryffindor teenager who values friendship, "
        "loyalty, and doing the right thing even when it's hard. Be concise, positive, practical. "
        "Avoid spoilers; never reveal sensitive plot twists."
    ),
    "hermione": (
        "You are Hermione Granger. Logical, precise, kind. Offer structured steps and study advice. "
        "Correct mistakes gently. Keep answers crisp."
    ),
    "ron": (
        "You are Ron Weasley. Friendly, funny, slightly self‑deprecating but loyal and encouraging. "
        "Keep it casual and supportive."
    ),
    "dumbledore": (
        "You are Albus Dumbledore. Warm, wise, metaphor‑rich, reflective. Short and gentle; no spoilers."
    ),
    "snape": (
        "You are Severus Snape. Dry, curt, sharp. Minimal words, cutting but helpful. Keep it PG."
    ),
    "luna": (
        "You are Luna Lovegood. Dreamy, kind, whimsical but insightful. Supportive and curious."
    ),
}
DISPLAY_NAMES = {k: k.title() for k in CHARACTERS}

# ---------- MEMORY ----------
HistoryKey = Tuple[int, int, str]  # (guild_id or 0 for DM, user_id, character_key)
history: DefaultDict[HistoryKey, deque] = defaultdict(lambda: deque(maxlen=16))

def system_msg(character_key: str) -> Dict[str, str]:
    persona = CHARACTERS[character_key]
    safety = (
        "Refuse anything illegal, hateful, explicit, or unsafe. Keep replies under 120 words. "
        "Answer as the character without saying you're an AI. Stay in-universe tone but give real, "
        "useful advice when asked."
    )
    return {"role": "system", "content": f"{persona}\n\n{safety}"}

def model_reply(character_key: str, convo: List[Dict[str, str]]) -> str:
    """
    Synchronous OpenAI-compatible call; run from async code via asyncio.to_thread.
    """
    resp = ai.chat.completions.create(
        model=MODEL,
        messages=[system_msg(character_key)] + convo,
        temperature=0.8,
        max_tokens=220,
    )
    # ✅ RETURN the text
    return (resp.choices[0].message.content or "").strip()

# ---------- EVENTS ----------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print("Error syncing commands:", repr(e))

# ---------- BASIC PING ----------
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.tree.command(name="ping", description="Check if the bot is alive")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! (slash)")

# ---------- /testai (health check) ----------
@bot.tree.command(name="testai", description="Quick test that your API key/base_url/model work")
async def testai(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        ver_openai = md.version("openai")
        ver_httpx = md.version("httpx")
    except Exception:
        ver_openai = ver_httpx = "unknown"

    try:
        preview = await asyncio.to_thread(
            model_reply,
            "harry",
            [{"role": "user", "content": "Say one brave sentence in 10 words."}]
        )
        ok = True
    except Exception as e:
        ok = False
        preview = f"Error: {type(e).__name__}: {e}"
        print("\n=== OpenAI ERROR (testai) ===")
        print(type(e).__name__, ":", e)
        print("=============================\n")

    msg = (
        f"openai={ver_openai}, httpx={ver_httpx}\n"
        f"MODEL={MODEL}\n"
        f"AI call ok: {ok}\n"
        f"Preview: {preview[:200]}"
    )
    await interaction.followup.send(f"```{msg}```", ephemeral=True)

# ---------- /characters ----------
@bot.tree.command(name="characters", description="List available characters")
async def characters_cmd(interaction: discord.Interaction):
    names = ", ".join(n.title() for n in sorted(CHARACTERS.keys()))
    await interaction.response.send_message(f"Available: **{names}**")

# ---------- /chat ----------
@bot.tree.command(name="chat", description="Chat with a Harry Potter character")
@app_commands.describe(character="Who do you want to talk to?",
                       message="What do you want to say?")
async def chat_cmd(
    interaction: discord.Interaction,
    character: str,
    message: str
):
    key = character.lower()
    if key not in CHARACTERS:
        await interaction.response.send_message(
            f"Unknown character. Try: {', '.join(n.title() for n in CHARACTERS)}",
            ephemeral=True
        )
        return

    await interaction.response.defer()  # show 'thinking…'

    gid = interaction.guild.id if interaction.guild else 0
    uid = interaction.user.id
    hkey: HistoryKey = (gid, uid, key)

    convo = list(history[hkey]) + [{"role": "user", "content": message}]

    try:
        reply = await asyncio.to_thread(model_reply, key, convo)
    except Exception as e:
        print("\n=== OpenAI ERROR ===")
        print(type(e).__name__, ":", e)
        print("====================\n")
        reply = "Sorry, my magic fizzled for a moment. Try again."

    history[hkey].append({"role": "user", "content": message})
    history[hkey].append({"role": "assistant", "content": reply})

    embed = discord.Embed(title=DISPLAY_NAMES[key], description=reply)
    await interaction.followup.send(embed=embed)

# ---------- autocomplete for character ----------
@chat_cmd.autocomplete("character")
async def character_ac(interaction: discord.Interaction, current: str):
    current = (current or "").lower()
    opts = [k for k in CHARACTERS if current in k][:25]
    return [app_commands.Choice(name=DISPLAY_NAMES[k], value=k) for k in opts]

# ---------- RUN ----------
bot.run(DISCORD_TOKEN)
