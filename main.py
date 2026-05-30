import discord
from discord.ext import commands
import random
import os

# ================= INTENTS =================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= STATE =================
auto_reply_enabled = False

jokes = [
    "Why did the bot cross the road? 🤖",
    "Python crashed again 💀",
    "UDP joke got lost.",
    "My CPU is emotionally unstable.",
    "I tried to code a joke... it errored."
]

auto_responses = [
    "🤖 Interesting!",
    "✨ Cool!",
    "👀 I see.",
    "🎉 Nice!",
    "😄 Tell me more!"
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
        elif "how are you" in msg:
            await message.reply("🤖 I'm doing great!")
        elif "bye" in msg:
            await message.reply("👋 Bye!")
        elif "ping" in msg:
            await message.reply("🏓 Pong!")
        else:
            await message.reply(random.choice(auto_responses))

    await bot.process_commands(message)

# =========================================================
# 📌 BASIC COMMANDS
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
        "**📌 Commands List**\n"
        "!ping - Check bot latency\n"
        "!joke - Random joke\n"
        "!rps <rock/paper/scissors>\n"
        "!coinflip\n"
        "!tictactoe @user\n"
        "!autoreply (admin only)\n"
    )

@bot.command()
@commands.has_permissions(administrator=True)
async def autoreply(ctx):
    global auto_reply_enabled
    auto_reply_enabled = not auto_reply_enabled

    await ctx.send(
        "🤖 Auto Reply ENABLED" if auto_reply_enabled else "🔇 Auto Reply DISABLED"
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
# 🎮 TIC TAC TOE (BUTTON GAME)
# =========================================================

class TicTacToeButton(discord.ui.Button):
    def __init__(self, x, y):
        super().__init__(label="➖", style=discord.ButtonStyle.secondary, row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view

        if interaction.user != view.current_player:
            return await interaction.response.send_message("⏳ Not your turn!", ephemeral=True)

        if view.board[self.y][self.x] != " ":
            return await interaction.response.send_message("❌ Already taken!", ephemeral=True)

        symbol = view.symbols[interaction.user]
        view.board[self.y][self.x] = symbol

        self.label = symbol
        self.disabled = True
        self.style = discord.ButtonStyle.success if symbol == "X" else discord.ButtonStyle.danger

        if view.check_winner(symbol):
            for b in view.children:
                b.disabled = True
            view.stop()

            return await interaction.response.edit_message(
                content=f"🏆 {interaction.user.mention} wins!",
                view=view
            )

        if view.is_draw():
            for b in view.children:
                b.disabled = True
            view.stop()

            return await interaction.response.edit_message(
                content="🤝 It's a draw!",
                view=view
            )

        view.switch_turn()

        await interaction.response.edit_message(
            content=f"🎮 Turn: {view.current_player.mention}",
            view=view
        )


class TicTacToeView(discord.ui.View):
    def __init__(self, p1, p2):
        super().__init__(timeout=120)

        self.p1 = p1
        self.p2 = p2
        self.current_player = p1

        self.symbols = {p1: "X", p2: "O"}
        self.board = [[" " for _ in range(3)] for _ in range(3)]

        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def switch_turn(self):
        self.current_player = self.p2 if self.current_player == self.p1 else self.p1

    def check_winner(self, s):
        b = self.board
        return (
            any(all(cell == s for cell in row) for row in b) or
            any(all(b[r][c] == s for r in range(3)) for c in range(3)) or
            all(b[i][i] == s for i in range(3)) or
            all(b[i][2 - i] == s for i in range(3))
        )

    def is_draw(self):
        return all(cell != " " for row in self.board for cell in row)

# =========================================================
# 🚀 READY
# =========================================================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# =========================================================
# RUN BOT
# =========================================================

bot.run(os.getenv("TOKEN"))
