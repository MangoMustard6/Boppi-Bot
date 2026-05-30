import discord
from discord.ext import commands
import random
import os

# ================= INTENTS =================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ================= BOT =================
bot = commands.Bot(command_prefix="!", intents=intents)

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

        symbol = view.symbols[view.current_player]
        view.board[self.y][self.x] = symbol

        self.label = symbol
        self.disabled = True
        self.style = discord.ButtonStyle.success if symbol == "X" else discord.ButtonStyle.danger

        if view.check_winner(symbol):
            for item in view.children:
                item.disabled = True
            view.stop()

            return await interaction.response.edit_message(
                content=f"🏆 {view.current_player.mention} wins!",
                view=view
            )

        if view.is_draw():
            for item in view.children:
                item.disabled = True
            view.stop()

            return await interaction.response.edit_message(
                content="🤝 Draw!",
                view=view
            )

        view.switch_turn()

        await interaction.response.edit_message(
            content=f"🎮 Turn: {view.current_player.mention} ({view.symbols[view.current_player]})",
            view=view
        )


class TicTacToeView(discord.ui.View):
    def __init__(self, p1, p2):
        super().__init__(timeout=120)

        self.player1 = p1
        self.player2 = p2
        self.current_player = p1

        self.symbols = {p1: "X", p2: "O"}
        self.board = [[" " for _ in range(3)] for _ in range(3)]

        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

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
# 🎲 GAMES (OTHER)
# =========================================================

@bot.command()
async def rps(ctx, choice: str):
    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)

    choice = choice.lower()

    if choice not in choices:
        return await ctx.send("Use: rock, paper, or scissors!")

    result = ""

    if choice == bot_choice:
        result = "🤝 Draw!"
    elif (
        (choice == "rock" and bot_choice == "scissors") or
        (choice == "paper" and bot_choice == "rock") or
        (choice == "scissors" and bot_choice == "paper")
    ):
        result = "🏆 You win!"
    else:
        result = "😈 You lose!"

    await ctx.send(f"You: {choice}\nBot: {bot_choice}\n{result}")


@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}")


# =========================================================
# 🤖 PREFIX TIC TAC TOE
# =========================================================

@bot.command()
async def tictactoe(ctx, opponent: discord.Member):
    view = TicTacToeView(ctx.author, opponent)

    await ctx.send(
        f"🎮 TicTacToe\n{ctx.author.mention} (X) vs {opponent.mention} (O)\nTurn: {ctx.author.mention}",
        view=view
    )


# =========================================================
# 🌐 SLASH COMMANDS (HYBRID SUPPORT)
# =========================================================

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


# slash tictactoe
@bot.tree.command(name="tictactoe", description="Play TicTacToe")
async def slash_ttt(interaction: discord.Interaction, opponent: discord.Member):
    view = TicTacToeView(interaction.user, opponent)

    await interaction.response.send_message(
        f"🎮 TicTacToe\n{interaction.user.mention} (X) vs {opponent.mention} (O)\nTurn: {interaction.user.mention}",
        view=view
    )


# slash rps
@bot.tree.command(name="rps", description="Rock Paper Scissors")
async def slash_rps(interaction: discord.Interaction, choice: str):
    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)

    choice = choice.lower()

    if choice not in choices:
        return await interaction.response.send_message("Use rock/paper/scissors")

    if choice == bot_choice:
        result = "🤝 Draw!"
    elif (
        (choice == "rock" and bot_choice == "scissors") or
        (choice == "paper" and bot_choice == "rock") or
        (choice == "scissors" and bot_choice == "paper")
    ):
        result = "🏆 You win!"
    else:
        result = "😈 You lose!"

    await interaction.response.send_message(
        f"You: {choice}\nBot: {bot_choice}\n{result}"
    )


# slash coinflip
@bot.tree.command(name="coinflip", description="Flip a coin")
async def slash_coin(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🪙 {random.choice(['Heads', 'Tails'])}"
    )


# =========================================================
# 🚀 RUN BOT
# =========================================================

bot.run(os.getenv("TOKEN"))
