import discord
from discord.ext import commands
import random
import os
import subprocess
import time

# ================= INTENTS =================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= STATE =================
auto_reply_enabled = False

jokes = [
    "Why did the bot cross the road? 🤖",
    "Python crashed again... surprise.",
    "I told a UDP joke. It didn’t arrive.",
    "My RAM is emotional today."
]

# =========================================================
# 🤖 AUTO REPLY SYSTEM
# =========================================================

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
            await message.reply("😄 Hi!")
        elif "bye" in msg:
            await message.reply("👋 Bye!")
        elif "ping" in msg:
            await message.reply("🏓 Pong!")
        else:
            await message.reply(random.choice([
                "🤖 Interesting!",
                "✨ Nice!",
                "👀 I see.",
                "🎉 Cool!"
            ]))

    await bot.process_commands(message)

# =========================================================
# 📌 FUN COMMANDS
# =========================================================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def joke(ctx):
    await ctx.send(random.choice(jokes))

@bot.command()
async def help(ctx):
    await ctx.send(
        "📌 Commands:\n"
        "!ping\n"
        "!joke\n"
        "!autoreply\n"
        "!rps <rock/paper/scissors>\n"
        "!coinflip\n"
        "!ffmpeg (upload video as attachment)\n"
    )

@bot.command()
@commands.has_permissions(administrator=True)
async def autoreply(ctx):
    global auto_reply_enabled
    auto_reply_enabled = not auto_reply_enabled

    await ctx.send(
        "🤖 Auto Reply Enabled!" if auto_reply_enabled
        else "🔇 Auto Reply Disabled!"
    )

# =========================================================
# 🎮 MINI GAMES
# =========================================================

@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}")

@bot.command()
async def rps(ctx, choice: str):
    options = ["rock", "
