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
    "I tried to code a joke... it crashed.",
    "Python is my sleep schedule.",
    "I would tell you a UDP joke, but you might not get it."
]

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
            await message.reply("😄 Hi there!")
        elif "how are you" in msg:
            await message.reply("🤖 I'm doing great!")
        elif "bye" in msg:
            await message.reply("👋 Goodbye!")
        elif "ping" in msg:
            await message.reply("🏓 Pong!")
        else:
            responses = [
                "🤖 Interesting!",
                "😄 Tell me more!",
                "👀 I see.",
                "✨ That's cool!",
                "🎉 Nice!"
            ]
            await message.reply(random.choice(responses))

    await bot.process_commands(message)

# ================= BASIC COMMANDS =================

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
async def roll(ctx):
    await ctx.send(f"🎲 You rolled: {random.randint(1, 6)}")

@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}")

@bot.command()
async def say(ctx, *, text):
    await ctx.send(text)

# ================= AUTOREPLY =================

@bot.command()
@commands.has_permissions(administrator=True)
async def autoreply(ctx):
    global auto_reply_enabled
    auto_reply_enabled = not auto_reply_enabled

    await ctx.send(
        "🤖 Auto Reply Enabled!" if auto_reply_enabled
        else "🔇 Auto Reply Disabled!"
    )

# ================= FUN COMMANDS =================

@bot.command()
async def joke2(ctx):
    extra_jokes = [
        "I'm not lazy, I'm just on energy-saving mode.",
        "Why do programmers hate nature? Too many bugs.",
        "I told my code a joke… it didn't compile."
    ]
    await ctx.send(random.choice(extra_jokes))

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.avatar.url)

@bot.command()
async def echo(ctx, *, msg):
    await ctx.send(f"📢 {msg}")

# ================= TIC TAC TOE PLACEHOLDER =================

@bot.command()
async def tictactoe(ctx):
    await ctx.send(
        "🎮 Tic-Tac-Toe\n\n"
        "1️⃣ 2️⃣ 3️⃣\n"
        "4️⃣ 5️⃣ 6️⃣\n"
        "7️⃣ 8️⃣ 9️⃣\n\n"
        "👉 (Interactive version coming soon)"
    )

# ================= RUN BOT =================

bot.run(os.getenv("TOKEN"))
@bot.command()
async def joke(ctx): await ctx.send(random.choice(jokes))

@bot.command()
async def help(ctx):
    await ctx.send("!ping !joke !rps !coinflip !tictactoe !autoreply")

@bot.command()
@commands.has_permissions(administrator=True)
async def autoreply(ctx):
    global auto
    auto = not auto
    await ctx.send("ON 🤖" if auto else "OFF 🔇")

# ================= GAMES =================
@bot.command()
async def coinflip(ctx):
    await ctx.send(random.choice(["Heads", "Tails"]))

@bot.command()
async def rps(ctx, c):
    b = random.choice(["rock","paper","scissors"])
    if c == b: r="Draw"
    elif (c,b) in [("rock","scissors"),("paper","rock"),("scissors","paper")]:
        r="Win"
    else: r="Lose"
    await ctx.send(f"You:{c} Bot:{b} {r}")

# ================= TIC TAC TOE =================
class B(discord.ui.Button):
    def __init__(s,x,y):
        super().__init__(label="➖", row=y); s.x=x; s.y=y

    async def callback(s,i):
        v=s.view
        if i.user!=v.turn: return await i.response.send_message("No turn",ephemeral=True)
        if v.b[s.y][s.x]!=" ": return await i.response.send_message("Taken",ephemeral=True)

        s.view.b[s.y][s.x]=v.sym[i.user]
        s.label=v.sym[i.user]
        s.disabled=True

        if v.win(v.sym[i.user]):
            for c in v.children: c.disabled=True
            return await i.response.edit_message(content=f"{i.user} wins!",view=v)

        v.turn = v.p2 if v.turn==v.p1 else v.p1

        await i.response.edit_message(content=f"Turn {v.turn}",view=v)

class V(discord.ui.View):
    def __init__(s,p1,p2):
        super().__init__(timeout=120)
        s.p1,s.p2=p1,p2
        s.turn=p1
        s.sym={p1:"X",p2:"O"}
        s.b=[[" "]*3 for _ in range(3)]
        for y in range(3):
            for x in range(3):
                s.add_item(B(x,y))

    def win(s,x):
        b=s.b
        return any(all(c==x for c in r) for r in b) or \
               any(all(b[i][c]==x for i in range(3)) for c in range(3)) or \
               all(b[i][i]==x for i in range(3)) or \
               all(b[i][2-i]==x for i in range(3))

@bot.command()
async def tictactoe(ctx, opp: discord.Member):
    await ctx.send(f"{ctx.author} vs {opp}", view=V(ctx.author,opp))

# ================= SLASH =================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Ready")

@bot.tree.command()
async def ping(i): await i.response.send_message("🏓 Pong!")

@bot.tree.command()
async def joke(i): await i.response.send_message(random.choice(jokes))

@bot.tree.command()
async def coinflip(i): await i.response.send_message(random.choice(["H","T"]))

@bot.tree.command()
async def autoreply(i):
    global auto
    auto = not auto
    await i.response.send_message("ON" if auto else "OFF")

@bot.tree.command()
async def rps(i,c):
    b=random.choice(["rock","paper","scissors"])
    await i.response.send_message(f"You:{c} Bot:{b}")

@bot.tree.command()
async def tictactoe(i,opp: discord.Member):
    await i.response.send_message(f"{i.user} vs {opp}", view=V(i.user,opp))

bot.run(os.getenv("TOKEN"))
