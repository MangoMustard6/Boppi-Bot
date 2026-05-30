import discord, random, os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

auto = False

jokes = [
    "Bot crossed road 🤖",
    "Python crashed 💀",
    "UDP joke lost.",
    "CPU emotional damage."
]

# ================= AUTO REPLY =================
@bot.event
async def on_message(m):
    global auto
    if m.author.bot: return

    if auto:
        t = m.content.lower()
        if "hello" in t: await m.reply("👋 Hi!")
        elif "hi" in t: await m.reply("😄 Hello!")
        elif "ping" in t: await m.reply("🏓 Pong!")
        else: await m.reply(random.choice(["🤖 ok", "✨ nice", "👀 hmm"]))

    await bot.process_commands(m)

# ================= COMMANDS =================
@bot.command()
async def ping(ctx): await ctx.send("🏓 Pong!")

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
