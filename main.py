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
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3,
```
        
