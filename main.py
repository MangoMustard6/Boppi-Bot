import discord
import os
import random
import requests
from discord.ext import commands

# ================= INTENTS =================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

auto_reply_enabled = False

jokes = [
    "Why did the bot cross the road? 🤖",
    "Python crashed again 💀",
    "I told a UDP joke... it didn't arrive.",
    "My CPU needs therapy."
]

# ================= EMBED HELPER =================

def make_embed(title, desc, color=0x00ffcc):
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

    # 🤖 AI CHAT MODE TRIGGER
    if bot.user.mentioned_in(message):
        await ai_chat(message, message.content)

    # 🤖 AUTO REPLY SYSTEM
    if auto_reply_enabled:
        msg = message.content.lower()

        if "hello" in msg:
            await message.reply("👋 Hello!")
        elif "hi" in msg:
            await message.reply("😄 Hi!")
        elif "ping" in msg:
            await message.reply("🏓 Pong!")
        else:
            await message.reply(random.choice(["🤖 Hmm...", "✨ Interesting!", "👀 I see"]))

    await bot.process_commands(message)

# ================= BASIC COMMANDS =================

@bot.command()
async def ping(ctx):
    embed = make_embed("🏓 Pong!", f"Latency: {round(bot.latency * 1000)}ms")
    await ctx.send(embed=embed)

@bot.command()
async def joke(ctx):
    embed = make_embed("😂 Joke", random.choice(jokes))
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = make_embed(
        "📌 Help Menu",
        "!ping\n!joke\n!ai <message>\n!autoreply\n!embedtest",
        0x3498db
    )
    await ctx.send(embed=embed)

# ================= AUTOREPLY =================

@bot.command()
@commands.has_permissions(administrator=True)
async def autoreply(ctx):
    global auto_reply_enabled
    auto_reply_enabled = not auto_reply_enabled

    msg = "ON 🤖" if auto_reply_enabled else "OFF 🔇"
    await ctx.send(embed=make_embed("Auto Reply", msg))

# ================= EMBED TEST =================

@bot.command()
async def embedtest(ctx):
    embed = discord.Embed(
        title="✨ Embed System",
        description="This is a clean embed message!",
        color=0x2ecc71
    )
    embed.add_field(name="Field 1", value="Hello world", inline=True)
    embed.add_field(name="Field 2", value="Discord Bot", inline=True)
    embed.set_footer(text="Powered by your bot")
    await ctx.send(embed=embed)

# ================= AI CHAT SYSTEM =================

async def ai_chat(message, user_text):
    prompt = user_text.replace(f"<@{bot.user.id}>", "").strip()

    if not prompt:
        return await message.reply("Ask me something 🤖")

    try:
        # Simple free AI endpoint (no key required)
        response = requests.get(
            f"https://api.popcat.xyz/chatbot?msg={prompt}&owner=Bot&botname=AI"
        ).json()

        reply = response.get("response", "I don't know that 😅")

        embed = discord.Embed(
            title="🤖 AI Response",
            description=reply,
            color=0x9b59b6
        )

        await message.reply(embed=embed)

    except:
        await message.reply("⚠️ AI is currently unavailable.")

# ================= AI COMMAND =================

@bot.command()
async def ai(ctx, *, msg):
    await ai_chat(ctx.message, msg)

# ================= RUN =================

bot.run(os.getenv("TOKEN"))
