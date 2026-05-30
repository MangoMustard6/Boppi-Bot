import discord
import os
import random
from discord.ext import commands

# ================= INTENTS =================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= STATE =================
auto_reply_enabled = False

jokes = [
    "Why did the bot cross the road? 🤖",
    "Python crashed again 💀",
    "UDP packets lost in space.",
    "My CPU is on vacation."
]

# ================= EMBED HELPER =================
def embed(title, desc, color=0x00ffcc):
    return discord.Embed(title=title, description=desc, color=color)

# ================= EVENTS =================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    global auto_reply_enabled

    if message.author.bot:
        return

    # AI trigger (mention bot)
    if bot.user in message.mentions:
        await ai_chat(message, message.content)

    # Auto reply system
    if auto_reply_enabled:
        msg = message.content.lower()

        if "hello" in msg:
            await message.reply("👋 Hello!")
        elif "hi" in msg:
            await message.reply("😄 Hi!")
        elif "ping" in msg:
            await message.reply("🏓 Pong!")
        else:
            await message.reply(random.choice(["🤖 Hmm...", "✨ Nice!", "👀 I see"]))

    await bot.process_commands(message)

# ================= BASIC COMMANDS =================

@bot.command()
async def ping(ctx):
    await ctx.send(embed=embed("🏓 Pong!", f"{round(bot.latency * 1000)}ms"))

@bot.command()
async def joke(ctx):
    await ctx.send(embed=embed("😂 Joke", random.choice(jokes)))

@bot.command()
async def hello(ctx):
    await ctx.send(f"👋 Hello {ctx.author.mention}")

@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}")

@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 {random.randint(1, 6)}")

@bot.command()
async def say(ctx, *, msg):
    await ctx.send(msg)

@bot.command()
async def help(ctx):
    await ctx.send("!ping !joke !ai !coinflip !roll !autoreply")

# ================= AUTOREPLY =================

@bot.command()
@commands.has_permissions(administrator=True)
async def autoreply(ctx):
    global auto_reply_enabled
    auto_reply_enabled = not auto_reply_enabled
    await ctx.send("ON 🤖" if auto_reply_enabled else "OFF 🔇")

# ================= SIMPLE AI (NO REQUESTS, NO AIOHTTP) =================

async def ai_chat(message, text):
    prompt = text.lower()

    # remove mention text
    prompt = prompt.replace(f"<@{bot.user.id}>", "").strip()

    if not prompt:
        await message.reply("Ask me something 🤖")
        return

    # SIMPLE "AI STYLE" RESPONSES (NO API = NO ERRORS)
    responses = [
        f"🤖 Interesting question: {prompt}",
        "✨ Let me think... that's cool!",
        "👀 I understand you.",
        "🧠 That's a deep one!",
        "🤖 I'm still learning, but that sounds cool!"
    ]

    await message.reply(embed=embed("AI Response", random.choice(responses), 0x9b59b6))

# ================= AI COMMAND =================

@bot.command()
async def ai(ctx, *, msg):
    await ai_chat(ctx.message, msg)

# ================= RUN BOT =================

token = os.getenv("TOKEN")

if not token:
    print("❌ TOKEN not found in environment variables!")
else:
    bot.run(token)
