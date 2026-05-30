import discord
import os
import random
from datetime import timedelta
from discord.ext import commands

# ================= INTENTS =================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# ================= STATE =================

auto_reply_enabled = False
warnings = {}

jokes = [
    "Why did the bot cross the road? 🤖",
    "I tried to code a joke... it crashed.",
    "Python is my sleep schedule.",
    "I would tell you a UDP joke, but you might not get it."
]

# ================= EMBED HELPER =================

def embed(title, description, color=0x00FFCC):
    return discord.Embed(
        title=title,
        description=description,
        color=color
    )

# ================= EVENTS =================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    global auto_reply_enabled

    if message.author.bot:
        return

    # AI mention trigger
    if bot.user in message.mentions:
        await ai_chat(message, message.content)

    # Auto reply
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
            await message.reply(
                random.choice([
                    "🤖 Interesting!",
                    "😄 Tell me more!",
                    "👀 I see.",
                    "✨ That's cool!",
                    "🎉 Nice!"
                ])
            )

    await bot.process_commands(message)

# ================= HELP =================

@bot.command()
async def help(ctx):
    await ctx.send(embed=embed(
        "📌 Bot Help",
        "**Fun Commands**\n"
        "!ping\n"
        "!joke\n"
        "!roll\n"
        "!coinflip\n"
        "!say <message>\n"
        "!ai <message>\n\n"

        "**System**\n"
        "!autoreply\n\n"

        "**Moderation**\n"
        "!modhelp"
    ))

@bot.command()
async def modhelp(ctx):
    await ctx.send(embed=embed(
        "🛡️ Moderation Commands",
        "!kick @user reason\n"
        "!ban @user reason\n"
        "!unban username\n"
        "!timeout @user minutes\n"
        "!clear amount\n"
        "!warn @user reason"
    ))

# ================= FUN COMMANDS =================

@bot.command()
async def ping(ctx):
    await ctx.send(
        embed=embed(
            "🏓 Pong!",
            f"Latency: {round(bot.latency * 1000)}ms"
        )
    )

@bot.command()
async def joke(ctx):
    await ctx.send(
        embed=embed(
            "😂 Joke",
            random.choice(jokes)
        )
    )

@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 You rolled: {random.randint(1, 6)}")

@bot.command()
async def coinflip(ctx):
    await ctx.send(
        f"🪙 {random.choice(['Heads', 'Tails'])}"
    )

@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)

# ================= AUTOREPLY =================

@bot.command()
@commands.has_permissions(administrator=True)
async def autoreply(ctx):
    global auto_reply_enabled

    auto_reply_enabled = not auto_reply_enabled

    await ctx.send(
        "🤖 Auto Reply Enabled!"
        if auto_reply_enabled
        else "🔇 Auto Reply Disabled!"
    )

# ================= SIMPLE AI =================

async def ai_chat(message, text):
    prompt = text.replace(
        f"<@{bot.user.id}>",
        ""
    ).strip()

    if not prompt:
        return await message.reply("Ask me something 🤖")

    responses = [
        f"🤖 Interesting question: {prompt}",
        "🧠 Let me think about that.",
        "✨ That's pretty cool.",
        "👀 I understand what you mean.",
        "🤖 I'm still learning, but that's interesting!"
    ]

    await message.reply(
        embed=embed(
            "🤖 AI Response",
            random.choice(responses),
            0x9B59B6
        )
    )

@bot.command()
async def ai(ctx, *, message):
    await ai_chat(ctx.message, message)

# ================= MODERATION =================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)

    await ctx.send(embed=embed(
        "👢 Member Kicked",
        f"{member.mention}\nReason: {reason}",
        0xE67E22
    ))

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)

    await ctx.send(embed=embed(
        "🔨 Member Banned",
        f"{member.mention}\nReason: {reason}",
        0xE74C3C
    ))

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, username):
    banned_users = await ctx.guild.bans()

    for entry in banned_users:
        user = entry.user

        if user.name == username:
            await ctx.guild.unban(user)

            return await ctx.send(
                embed=embed(
                    "♻️ Member Unbanned",
                    str(user)
                )
            )

    await ctx.send("❌ User not found.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int):
    await member.timeout(
        timedelta(minutes=minutes)
    )

    await ctx.send(embed=embed(
        "⏳ Timeout Applied",
        f"{member.mention}\nDuration: {minutes} minutes"
    ))

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)

    msg = await ctx.send(embed=embed(
        "🧹 Messages Cleared",
        f"Deleted {amount} messages"
    ))

    await msg.delete(delay=3)

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    warnings[member.id] = warnings.get(member.id, 0) + 1

    await ctx.send(embed=embed(
        "⚠️ Warning Issued",
        f"{member.mention}\n"
        f"Reason: {reason}\n"
        f"Warnings: {warnings[member.id]}"
    ))

# ================= RUN =================

token = os.getenv("TOKEN")

if not token:
    print("❌ TOKEN not found!")
else:
    bot.run(token)
