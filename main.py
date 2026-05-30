import discord
import os
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

auto_reply_enabled = False

jokes = [
"Why did the bot cross the road? 🤖",
"I tried to code a joke... it crashed.",
"Python is my sleep schedule.",
"I would tell you a UDP joke, but you might not get it."
]

@bot.event
async def on_ready():
print(f"Logged in as {bot.user}")

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

```
auto_reply_enabled = not auto_reply_enabled

if auto_reply_enabled:
    await ctx.send("🤖 Auto Reply Enabled!")
else:
    await ctx.send("🔇 Auto Reply Disabled!")
```

@bot.command()
async def tictactoe(ctx):
board = ["1", "2", "3",
"4", "5", "6",
"7", "8", "9"]

```
current = "❌"

def show_board():
    return (
        f"{board[0]} | {board[1]} | {board[2]}\n"
        f"---------\n"
        f"{board[3]} | {board[4]} | {board[5]}\n"
        f"---------\n"
        f"{board[6]} | {board[7]} | {board[8]}"
    )

await ctx.send(
    "🎮 Tic-Tac-Toe\n"
    "Type a number from 1-9 to place your mark.\n\n"
    + show_board()
)

def check_win():
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c]:
            return True
    return False

for turn in range(9):

    def check(m):
        return (
            m.author == ctx.author
            and m.channel == ctx.channel
            and m.content.isdigit()
        )

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
    except:
        await ctx.send("⏰ Game timed out!")
        return

    pos = int(msg.content) - 1

    if pos < 0 or pos > 8 or board[pos] in ["❌", "⭕"]:
        await ctx.send("❌ Invalid move!")
        continue

    board[pos] = current

    await ctx.send(show_board())

    if check_win():
        await ctx.send(f"🏆 {current} wins!")
        return

    current = "⭕" if current == "❌" else "❌"

await ctx.send("🤝 It's a draw!")
```

@bot.event
async def on_message(message):
global auto_reply_enabled

```
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

    elif "ping" in msg:
        await message.reply("🏓 Pong!")

    elif "bye" in msg:
        await message.reply("👋 Goodbye!")

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
```

bot.run(os.getenv("TOKEN"))
