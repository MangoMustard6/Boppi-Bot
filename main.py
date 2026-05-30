import discord
import os
import random
import aiohttp
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
    "UDP joke lost in transit.",
    "My CPU needs coffee."
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

    # AI trigger via mention
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
    await ctx.send(embed=embed("🏓 Pong!", f"{round(bot.latency*1000)}ms"))

@bot.command()
async def joke(ctx):
    await ctx.send(embed=embed("😂 Joke", random.choice(jokes)))

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! 👋")

@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}")

@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 {random.randint(1,6)}")

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

# ================= AI CHAT (SAFE FIXED VERSION) =================

async def ai_chat(message, text):
    prompt = text.replace(f"<@{bot.user.id}>", "").strip()

    if not prompt:
        return await message.reply("Ask me something 🤖")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.popcat.xyz/chatbot?msg={prompt}&owner=Bot&botname=AI"
            ) as resp:
                data = await resp.json()

        reply = data.get("response", "I don't know that 😅")

        await message.reply(embed=embed("🤖 AI", reply, 0x9b59b6))

    except:
        await message.reply("⚠️ AI service unavailable.")

# ================= AI COMMAND =================

@bot.command()
async def ai(ctx, *, msg):
    await ai_chat(ctx.message, msg)

# ================= RUN BOT =================

bot.run(os.getenv("TOKEN"))
