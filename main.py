from datetime import datetime
import discord
from discord.ext import commands
import logging
import sys

import sub

prefixes = ['au', 'Au']
with open("./token.txt", encoding = "utf-8") as file:
    token = file.read()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = prefixes, intents = intents)

@bot.event
async def on_ready():
    line = f"on_ready {discord.__version__}"
    logging.info(line)
    print(line)

def get_current_datetime_str():
    return str(datetime.now()).replace(':', '-')

def update_logging_file():
    logging.basicConfig(filename=f"log/{get_current_datetime_str()}.log", encoding="utf-8", level=logging.DEBUG)

logging_count = 0
update_logging_file()

@bot.event
async def on_error(event, *args, **kwargs):
    info = sys.exc_info()
    line = f"{get_current_datetime_str()}\t{event}\t{str(info)}"
    logging.error(line)
    print(line)
    
    global logging_count
    logging_count += 1
    if logging_count > 200:
        update_logging_file()

@bot.command()
async def b(ctx: commands.Context):
    await sub.begin(ctx)

@bot.command()
async def begin(ctx: commands.Context):
    await sub.begin(ctx)

@bot.command()
async def o(ctx: commands.Context):
    await sub.open(ctx)

@bot.command()
async def open(ctx: commands.Context):
    await sub.open(ctx)

@bot.command()
async def c(ctx: commands.Context):
    await sub.close(ctx)

@bot.command()
async def join(ctx: commands.Context):
    await sub.close(ctx)

@bot.command()
async def k(ctx: commands.Context, arg: str):
    await sub.kill(ctx, arg)

@bot.command()
async def kill(ctx: commands.Context, arg: str):
    await sub.kill(ctx, arg)

@bot.command()
async def r(ctx: commands.Context):
    await sub.reset(ctx)

@bot.command()
async def reset(ctx: commands.Context):
    await sub.reset(ctx)

@bot.command()
async def e(ctx: commands.Context):
    await sub.end(ctx)

@bot.command()
async def end(ctx: commands.Context):
    await sub.end(ctx)

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if bot.user.id in [member.id for member in message.mentions]:
        await sub.begin(commands.Context(message = message, prefix = ''))
        return
    
    for prefix in prefixes:
        if prefix == message.content:
            await message.channel.send(f"""\
To play, first, gather members in a voice channel, and then call beginning command.
When someone passed away, call killing command.
A prefix is needed to call commands.
Prefixes:
    {", ".join(prefixes)}
Commands:
    b, begin:\tbegin the game
    o, open:\topen a discussion
    c, close\tclose the discussion
    k, kill N\tkill N
    r, reset\teset the game
    e, end\tend the game""")
            return
    
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction: discord.Reaction, user):
    await sub.on_reaction_add(reaction, user)

@bot.event
async def on_reaction_remove(reaction: discord.Reaction, user):
    await sub.on_reaction_remove(reaction, user)

bot.run(token)