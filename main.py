import discord
import os
import random
import asyncio
from discord.ext import commands

# ================= BOT SETUP =================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="b!",
    intents=intents,
    help_command=None
)

# ================= DATA =================

gd_scores = {}

jokes = [
    "Why did the bot cross the road? 🤖",
    "I tried to code a joke... it crashed.",
    "Python is my sleep schedule.",
    "I would tell you a UDP joke, but you might not get it."
]

# ================= EMBEDS =================

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

# ================= HELP =================

@bot.command()
async def help(ctx):
    await ctx.send(embed=embed(
        "📌 Help Menu",
        "**Fun Commands**\n"
        "!ping\n"
        "!joke\n"
        "!hello\n"
        "!coinflip\n"
        "!roll\n"
        "!say <message>\n\n"
        "**Geometry Dash**\n"
        "!gd <difficulty> <mode>\n"
        "!gdleaderboard\n\n"
        "🎨 Difficulties: Easy, Normal, Hard, Demon\n"
        "🕹️ Modes: Cube, Ship, Wave"
    ))

# ================= FUN COMMANDS =================

@bot.command()
async def ping(ctx):
    await ctx.send(embed=embed(
        "🏓 Pong!",
        f"Latency: {round(bot.latency * 1000)}ms"
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
async def coinflip(ctx):
    await ctx.send(
        f"🪙 {random.choice(['Heads', 'Tails'])}"
    )

@bot.command()
async def roll(ctx):
    await ctx.send(
        f"🎲 You rolled {random.randint(1, 6)}"
    )

@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)

# ================= GEOMETRY DASH MINI GAME =================

class GDView(discord.ui.View):
    def __init__(self, player, difficulty="Normal", mode="Cube"):
        super().__init__(timeout=60)

        self.player = player
        self.score = 0
        self.coins = 0
        self.alive = True
        self.jumping = False

        self.difficulty = difficulty
        self.mode = mode

        speeds = {
            "Easy": 3,
            "Normal": 2,
            "Hard": 1.5,
            "Demon": 1
        }

        self.delay = speeds[difficulty]

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
                "❌ This isn't your game!",
                ephemeral=True
            )

        self.jumping = True
        await interaction.response.defer()

    async def run_game(self, message):
        gd_messages = [
            "🔥 FIRE IN THE HOLE!",
            "🎵 Stereo Madness!",
            "⚡ Wave section!",
            "🛸 Ship section!",
            "⭐ Coin collected!",
            "💀 Demon difficulty!"
        ]

        while self.alive:
            await asyncio.sleep(self.delay)

            spike = random.randint(1, 4)

            if spike == 1:
                if self.jumping:
                    self.score += 1
                    self.jumping = False

                    if random.randint(1, 5) == 1:
                        self.coins += 1

                    await message.edit(
                        content=(
                            f"🟦 Jump successful!\n"
                            f"🏆 Score: {self.score}\n"
                            f"⭐ Coins: {self.coins}\n"
                            f"🎨 Difficulty: {self.difficulty}\n"
                            f"🕹️ Mode: {self.mode}\n\n"
                            f"{random.choice(gd_messages)}"
                        ),
                        view=self
                    )
                else:
                    self.alive = False

                    gd_scores[self.player.id] = max(
                        gd_scores.get(self.player.id, 0),
                        self.score
                    )

                    await message.edit(
                        content=(
                            f"💀 GAME OVER!\n\n"
                            f"🏆 Score: {self.score}\n"
                            f"⭐ Coins: {self.coins}"
                        ),
                        view=None
                    )
            else:
                self.score += 1

                await message.edit(
                    content=(
                        f"⬜ Safe...\n"
                        f"🏆 Score: {self.score}\n"
                        f"⭐ Coins: {self.coins}\n"
                        f"🎨 Difficulty: {self.difficulty}\n"
                        f"🕹️ Mode: {self.mode}"
                    ),
                    view=self
                )

@bot.command()
async def gd(ctx, difficulty="Normal", mode="Cube"):
    difficulty = difficulty.capitalize()
    mode = mode.capitalize()

    valid_difficulties = [
        "Easy",
        "Normal",
        "Hard",
        "Demon"
    ]

    valid_modes = [
        "Cube",
        "Ship",
        "Wave"
    ]

    if difficulty not in valid_difficulties:
        return await ctx.send(
            "❌ Difficulties: Easy, Normal, Hard, Demon"
        )

    if mode not in valid_modes:
        return await ctx.send(
            "❌ Modes: Cube, Ship, Wave"
        )

    view = GDView(
        ctx.author,
        difficulty,
        mode
    )

    msg = await ctx.send(
        f"🎮 Geometry Dash Mini\n"
        f"🎨 Difficulty: {difficulty}\n"
        f"🕹️ Mode: {mode}\n\n"
        f"Press **Jump** to avoid spikes!",
        view=view
    )

    asyncio.create_task(
        view.run_game(msg)
    )

# ================= LEADERBOARD =================

@bot.command()
async def gdleaderboard(ctx):
    if not gd_scores:
        return await ctx.send(
            "🏆 No scores recorded yet!"
        )

    sorted_scores = sorted(
        gd_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    leaderboard = ""

    for pos, (user_id, score) in enumerate(
        sorted_scores[:10],
        start=1
    ):
        user = bot.get_user(user_id)

        if user:
            leaderboard += (
                f"{pos}. {user.name} — {score}\n"
            )

    await ctx.send(
        embed=embed(
            "🏆 Geometry Dash Leaderboard",
            leaderboard
        )
    )

# ================= RUN BOT =================

token = os.getenv("TOKEN")

if not token:
    print("❌ TOKEN environment variable not found!")
else:
    bot.run(token)
