import discord
import os
import random
import asyncio
from discord.ext import commands

# ================= BOT =================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="bop!",
    intents=intents,
    help_command=None
)

# ================= DATA =================

gd_scores = {}

jokes = [
    "Why did the bot cross the road? 🤖",
    "Python crashed again 💀",
    "UDP packets got lost.",
    "My CPU is on vacation."
]

# ================= EMBEDS =================

def embed(title, desc, color=0x00FFCC):
    return discord.Embed(
        title=title,
        description=desc,
        color=color
    )

# ================= EVENTS =================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"discord.py version: {discord.__version__}")

# ================= HELP =================

@bot.command()
async def help(ctx):
    await ctx.send(embed=embed(
        "📌 Commands",
        "**Fun**\n"
        "!ping\n"
        "!joke\n"
        "!hello\n"
        "!roll\n"
        "!coinflip\n"
        "!say <message>\n\n"
        "**Geometry Dash**\n"
        "!gd Easy\n"
        "!gd Normal\n"
        "!gd Hard\n"
        "!gd Demon\n"
        "!gdleaderboard"
    ))

# ================= FUN =================

@bot.command()
async def ping(ctx):
    await ctx.send(embed=embed(
        "🏓 Pong!",
        f"{round(bot.latency * 1000)}ms"
    ))

@bot.command()
async def joke(ctx):
    await ctx.send(embed=embed(
        "😂 Joke",
        random.choice(jokes)
    ))

@bot.command()
async def hello(ctx):
    await ctx.send(f"👋 Hello {ctx.author.mention}!")

@bot.command()
async def roll(ctx):
    await ctx.send(
        f"🎲 {random.randint(1,6)}"
    )

@bot.command()
async def coinflip(ctx):
    await ctx.send(
        f"🪙 {random.choice(['Heads','Tails'])}"
    )

@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)

# ================= GEOMETRY DASH =================

class GDView(discord.ui.View):
    def __init__(self, player, difficulty):
        super().__init__(timeout=120)

        self.player = player
        self.score = 0
        self.coins = 0
        self.jumping = False
        self.alive = True

        self.track = ["⬜"] * 12
        self.player_pos = 2

        self.delay = {
            "Easy": 2.0,
            "Normal": 1.5,
            "Hard": 1.0,
            "Demon": 0.7
        }[difficulty]

        self.difficulty = difficulty

    @discord.ui.button(
        label="⬆️ Jump",
        style=discord.ButtonStyle.green
    )
    async def jump(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if interaction.user != self.player:
            return await interaction.response.send_message(
                "❌ Not your game!",
                ephemeral=True
            )

        self.jumping = True
        await interaction.response.defer()

    def render_track(self):
        display = self.track.copy()
        display[self.player_pos] = "🟦"
        return "".join(display)

    async def run(self, message):
        while self.alive:

            await asyncio.sleep(self.delay)

            self.track.pop(0)

            roll = random.randint(1, 10)

            if roll <= 2:
                self.track.append("🔺")
            elif roll == 3:
                self.track.append("⭐")
            else:
                self.track.append("⬜")

            tile = self.track[self.player_pos]

            if tile == "⭐":
                self.coins += 1
                self.track[self.player_pos] = "⬜"

            elif tile == "🔺":

                if self.jumping:
                    self.score += 5
                    self.jumping = False
                else:
                    self.alive = False
                    break

            else:
                self.score += 1

            text = (
                f"🎮 Geometry Dash ({self.difficulty})\n"
                f"🏆 Score: {self.score}\n"
                f"⭐ Coins: {self.coins}\n\n"
                f"{self.render_track()}"
            )

            await message.edit(
                content=text,
                view=self
            )

        gd_scores[self.player.id] = max(
            gd_scores.get(self.player.id, 0),
            self.score
        )

        for child in self.children:
            child.disabled = True

        await message.edit(
            content=(
                f"💀 GAME OVER\n\n"
                f"🏆 Score: {self.score}\n"
                f"⭐ Coins: {self.coins}"
            ),
            view=self
        )

# ================= GD COMMAND =================

@bot.command()
async def gd(ctx, difficulty="Normal"):

    difficulty = difficulty.capitalize()

    if difficulty not in [
        "Easy",
        "Normal",
        "Hard",
        "Demon"
    ]:
        return await ctx.send(
            "Use: Easy, Normal, Hard, Demon"
        )

    view = GDView(
        ctx.author,
        difficulty
    )

    msg = await ctx.send(
        f"🎮 Starting Geometry Dash ({difficulty})...\n\n"
        f"{view.render_track()}",
        view=view
    )

    asyncio.create_task(
        view.run(msg)
    )

# ================= LEADERBOARD =================

@bot.command()
async def gdleaderboard(ctx):

    if not gd_scores:
        return await ctx.send(
            "🏆 No scores yet!"
        )

    board = sorted(
        gd_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    text = ""

    for pos, (uid, score) in enumerate(
        board[:10],
        start=1
    ):
        user = bot.get_user(uid)

        if user:
            text += (
                f"{pos}. {user.name} — {score}\n"
            )

    await ctx.send(embed=embed(
        "🏆 Geometry Dash Leaderboard",
        text
    ))

# ================= RUN =================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("TOKEN environment variable missing.")
else:
    bot.run(TOKEN)
