import discord
import os
import random
from discord.ext import commands

# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.message_content = True

# ---------- BOT SETUP ----------
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- GLOBAL STATE ----------
auto_reply_enabled = False

# ---------- DATA ----------
jokes = [
    "Why did the bot cross the road? 🤖",
    "I tried to code a joke... it crashed.",
    "Python is my sleep schedule.",
    "I would tell you a UDP joke, but you might not get it."
]

auto_responses = [
    "🤖 Interesting!",
    "😄 Tell me more!",
    "👀 I see.",
    "✨ That's cool!",
    "🎉 Nice!"
]

# ---------- EVENTS ----------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    global auto_reply_enabled

    if message.author.bot:
        return

    if auto_reply_enabled:
        msg = message.content.lower()

        if "hello" in msg:
            await message.reply("👋 Hello!")
        elif "hi" in msg:
            await message.reply("😄 Hi there!")
        elif "how are you" in msg:
            await message.reply("🤖 I'm doing great!")
        elif "bye" in msg:
            await message.reply("👋 Goodbye!")
        elif "ping" in msg:
            await message.reply("🏓 Pong!")
        else:
            await message.reply(random.choice(auto_responses))

    await bot.process_commands(message)

# ---------- COMMANDS ----------
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def joke(ctx):
    await ctx.send(random.choice(jokes))

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! 👋")

@bot.command()
@commands.has_permissions(administrator=True)
async def autoreply(ctx):
    global auto_reply_enabled
    auto_reply_enabled = not auto_reply_enabled

    if auto_reply_enabled:
        await ctx.send("🤖 Auto Reply Enabled!")
    else:
        await ctx.send("🔇 Auto Reply Disabled!")

@bot.command()
async def tictactoe(ctx):
    board = (
        "🎮 Tic-Tac-Toe\n\n"
        "1️⃣ 2️⃣ 3️⃣\n"
        "4️⃣ 5️⃣ 6️⃣\n"
        "7️⃣ 8️⃣ 9️⃣\n\n"
        "Type numbers in chat to play manually!"
    )
    await ctx.send(board)

# ---------- RUN BOT ----------
bot.run(os.getenv("TOKEN"))
