import discord
import os
import random
from discord.ext import commands

# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # recommended for mentions/features

# ---------- BOT ----------
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- GLOBAL STATE ----------
auto_reply_enabled = False

# ---------- DATA ----------
jokes = [
    "Why did the bot cross the road? 🤖",
    "I tried to code a joke... it crashed.",
    "Python is my sleep schedule.",
    "I would tell you a UDP joke, but you might not get it."
]

auto_responses = [
    "🤖 Interesting!",
    "😄 Tell me more!",
    "👀 I see.",
    "✨ That's cool!",
    "🎉 Nice!"
]

# =========================================================
# 🎮 TIC TAC TOE GAME
# =========================================================

class TicTacToeButton(discord.ui.Button):
    def __init__(self, x, y):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="➖",
            row=y
        )
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view

        # already taken
        if view.board[self.y][self.x] != " ":
            return await interaction.response.send_message(
                "❌ That spot is already taken!", ephemeral=True
            )

        # not your turn
        if interaction.user != view.current_player:
            return await interaction.response.send_message(
                "⏳ It's not your turn!", ephemeral=True
            )

        symbol = view.symbols[view.current_player]

        # place move
        view.board[self.y][self.x] = symbol
        self.label = symbol
        self.disabled = True

        if symbol == "X":
            self.style = discord.ButtonStyle.success
        else:
            self.style = discord.ButtonStyle.danger

        # check win
        if view.check_winner():
            for child in view.children:
                child.disabled = True
            view.stop()

            await interaction.response.edit_message(
                content=f"🏆 {view.current_player.mention} wins!",
                view=view
            )
            return

        # check draw
        if view.is_draw():
            for child in view.children:
                child.disabled = True
            view.stop()

            await interaction.response.edit_message(
                content="🤝 It's a draw!",
                view=view
            )
            return

        # switch turn
        view.switch_turn()

        await interaction.response.edit_message(
            content=f"🎮 Turn: {view.current_player.mention} ({view.symbols[view.current_player]})",
            view=view
        )


class TicTacToeView(discord.ui.View):
    def __init__(self, player1, player2):
        super().__init__(timeout=120)

        self.player1 = player1
        self.player2 = player2
        self.current_player = player1

        self.symbols = {
            player1: "X",
            player2: "O"
        }

        self.board = [[" " for _ in range(3)] for _ in range(3)]

        # create buttons
        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def switch_turn(self):
        self.current_player = (
            self.player2 if self.current_player == self.player1 else self.player1
        )

    def check_winner(self):
        b = self.board

        win_lines = [
            # rows
            [b[0][0], b[0][1], b[0][2]],
            [b[1][0], b[1][1], b[1][2]],
            [b[2][0], b[2][1], b[2][2]],

            # columns
            [b[0][0], b[1][0], b[2][0]],
            [b[0][1], b[1][1], b[2][1]],
            [b[0][2], b[1][2], b[2][2]],

            # diagonals
            [b[0][0], b[1][1], b[2][2]],
            [b[0][2], b[1][1], b[2][0]],
        ]

        for line in win_lines:
            if line[0] != " " and line.count(line[0]) == 3:
                return True

        return False

    def is_draw(self):
        return all(cell != " " for row in self.board for cell in row)


# =========================================================
# 🤖 EVENTS
# =========================================================

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
            await message.reply(random.choice(auto_responses))

    await bot.process_commands(message)


# =========================================================
# 📌 COMMANDS
# =========================================================

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
    auto_reply_enabled = not auto_reply_enabled

    if auto_reply_enabled:
        await ctx.send("🤖 Auto Reply Enabled!")
    else:
        await ctx.send("🔇 Auto Reply Disabled!")


@bot.command()
async def tictactoe(ctx, opponent: discord.Member):
    if opponent.bot:
        return await ctx.send("🤖 You can't play against a bot!")

    view = TicTacToeView(ctx.author, opponent)

    await ctx.send(
        f"🎮 Tic-Tac-Toe Started!\n"
        f"{ctx.author.mention} (X) vs {opponent.mention} (O)\n\n"
        f"Turn: {ctx.author.mention} (X)",
        view=view
    )


# =========================================================
# 🚀 RUN BOT
# =========================================================

bot.run(os.getenv("TOKEN"))
