import discord
import os
import random
from discord.ext import commands
from datetime import timedelta

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
warnings = {}  # user_id -> count

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

# ================= FUN COMMANDS =================

@bot.command()
async def ping(ctx):
    await ctx.send(embed=embed("🏓 Pong!", f"{round(bot.latency * 1000)}ms"))

@bot.command()
async def joke(ctx):
    await ctx.send(embed=embed("😂 Joke", random.choice(jokes)))

@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 {random.randint(1, 6)}")

@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}")

# ================= AUTOREPLY =================

@bot.command()
@commands.has_permissions(administrator=True)
async def autoreply(ctx):
    global auto_reply_enabled
    auto_reply_enabled = not auto_reply_enabled
    await ctx.send("ON 🤖" if auto_reply_enabled else "OFF 🔇")

# ================= MODERATION COMMANDS =================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(embed=embed("👢 Kicked", f"{member} was kicked\nReason: {reason}", 0xff9900))

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(embed=embed("🔨 Banned", f"{member} was banned\nReason: {reason}", 0xff0000))

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            await ctx.send(embed=embed("♻️ Unbanned", f"{user} was unbanned"))
            return

    await ctx.send("User not found.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration)
    await ctx.send(embed=embed("⏳ Timeout", f"{member} muted for {minutes} minutes"))

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(embed=embed("🧹 Cleared", f"Deleted {amount} messages", 0x00ff00), delete_after=3)

# ================= WARN SYSTEM =================

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="No reason"):
    uid = member.id
    warnings[uid] = warnings.get(uid, 0) + 1

    await ctx.send(embed=embed(
        "⚠️ Warned",
        f"{member} has been warned\nReason: {reason}\nTotal warns: {warnings[uid]}",
        0xffcc00
    ))

    if warnings[uid] >= 3:
        await member.kick(reason="3 warnings reached")
        await ctx.send(f"👢 {member} was kicked for 3 warnings")

# ================= MOD HELP =================

@bot.command()
async def modhelp(ctx):
    await ctx.send(embed=embed(
        "🛡️ Moderation Commands",
        "!kick @user reason\n!ban @user reason\n!unban name\n!timeout @user minutes\n!clear number\n!warn @user reason",
        0x3498db
    ))

# ================= RUN =================

token = os.getenv("TOKEN")

if not token:
    print("❌ TOKEN missing")
else:
    bot.run(token)
