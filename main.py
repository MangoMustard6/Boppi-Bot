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

bot = commands.Bot(command_prefix="bop!", intents=intents)

# ================= STATE =================
auto_reply_enabled = False

jokes = [
    "Why did the bot cross the road? 🤖",
    "Python crashed again 💀",
    "UDP joke not delivered.",
    "My CPU is emotionally unstable."
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
                "✨ Cool!",
                "👀 I see.",
                "🎉 Nice!"
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
        "!ffmpeg (upload video)\n"
    )

@bot.command()
@commands.has_permissions(administrator=True)
async def autoreply(ctx):
    global auto_reply_enabled
    auto_reply_enabled = not auto_reply_enabled

    await ctx.send(
        "🤖 Auto Reply Enabled!" if auto_reply_enabled else "🔇 Auto Reply Disabled!"
    )

# =========================================================
# 🎮 MINI GAMES
# =========================================================

@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}")

@bot.command()
async def rps(ctx, choice: str):
    options = ["rock", "paper", "scissors"]
    bot_choice = random.choice(options)

    choice = choice.lower()

    if choice not in options:
        return await ctx.send("Use rock, paper, or scissors!")

    if choice == bot_choice:
        result = "🤝 Draw!"
    elif (choice == "rock" and bot_choice == "scissors") or \
         (choice == "paper" and bot_choice == "rock") or \
         (choice == "scissors" and bot_choice == "paper"):
        result = "🏆 You win!"
    else:
        result = "😈 You lose!"

    await ctx.send(f"You: {choice}\nBot: {bot_choice}\n{result}")

# =========================================================
# 🎛️ FFmpeg VIDEO EDITOR COMMAND
# =========================================================

@bot.command()
async def ffmpeg(ctx):
    if not ctx.message.attachments:
        return await ctx.send("📎 Upload a video with the command!")

    file = ctx.message.attachments[0]

    if not file.filename.endswith((".mp4", ".mov", ".mkv")):
        return await ctx.send("❌ Please upload a video file!")

    start = time.time()

    input_path = f"input_{file.filename}"
    output_path = f"output_{file.filename}"

    await file.save(input_path)

    # 🎛️ FFmpeg FILTERS (edit here)
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vf", "scale=1280:720,eq=contrast=1.2:brightness=0.05",
        "-preset", "fast",
        "-y",
        output_path
    ]

    await ctx.send("🎛️ Processing video...")

    subprocess.run(ffmpeg_cmd)

    end = time.time()

    await ctx.send(
        content=f"✅ Done in {round(end - start, 2)}s",
        file=discord.File(output_path)
    )

    os.remove(input_path)
    os.remove(output_path)

# =========================================================
# 🚀 RUN BOT
# =========================================================

bot.run(os.getenv("TOKEN"))
