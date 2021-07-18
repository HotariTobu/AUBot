import discord
from discord.ext import commands

from icon import OperatorIconKeys, OPERATOR_ICONS, PLAYER_ICONS
from game import Game
from player import Player

games = {}

OPERATOR_ICONS_STR = f"""\
{OPERATOR_ICONS[OperatorIconKeys.DISCUSSION]}:\tswitch discussion
{OPERATOR_ICONS[OperatorIconKeys.KILL]}:\tkill N
{OPERATOR_ICONS[OperatorIconKeys.RESET]}:\treset the game
{OPERATOR_ICONS[OperatorIconKeys.END]}:\tend the game
"""

def get_id_from(ctx: commands.Context):
    return ctx.author.voice.channel.id

async def update_embed(game: Game):
    description = ""
    for player in game.players:
        if player.is_killed:
            description += f"||{player.emoji}:\t{player.name}||\n"
        else:
            description += f"{player.emoji}:\t{player.name}\n"
    description += f"\n{OPERATOR_ICONS_STR}"

    embed = discord.Embed(description = description)
    await game.message.edit(embed = embed)

async def begin(ctx: commands.Context):
    voice = ctx.author.voice
    if voice is None:
        await ctx.send("You are not connected to any voice channel.")
        return

    if get_id_from(ctx) in games:
        await ctx.send("The game has already begun!")
        return
    
    await voice.channel.connect()

    players = []
    index = 0
    for member in voice.channel.members:
        if not member.bot:
            players.append(Player(PLAYER_ICONS[index], member))
            index += 1
    
    message = await ctx.send("Let's enjoy!")
    game = Game(players, message)
    games[get_id_from(ctx)] = game
    
    await update_embed(game)
    for key in OperatorIconKeys:
        await message.add_reaction(OPERATOR_ICONS[key])

failed_text = "Pls. begin a game before calling some commands."

async def open(ctx: commands.Context):
    game = games.get(get_id_from(ctx))
    if game is None:
        await ctx.send(failed_text)
        return

    await game.open()

async def close(ctx: commands.Context):
    game = games.get(get_id_from(ctx))
    if game is None:
        await ctx.send(failed_text)
        return

    await game.close()

async def kill(ctx: commands.Context, arg: str):
    game = games.get(get_id_from(ctx))
    if game is None:
        await ctx.send(failed_text)
        return
        
    if (await game.kill(arg)):
        await ctx.send(f"There is no player tagged or named {arg}")
    else:
        await update_embed(game)

async def reset(ctx: commands.Context):
    game = games.get(get_id_from(ctx))
    if game is None:
        await ctx.send(failed_text)
        return

    await game.reset()
    await update_embed(game)

async def end(ctx: commands.Context):
    game = games.pop(get_id_from(ctx), None)
    if game is None:
        await ctx.send(failed_text)
        return

    await ctx.voice_client.disconnect()
    await game.reset()
    await game.message.delete()
    if (not game.kill_message is None):
        await game.kill_message.delete()

async def on_reaction_add(reaction: discord.Reaction, user):
    game = games.get(user.voice.channel.id)
    if game is None or reaction.message.author.id == user.id:
        return

    ctx = commands.Context(message = game.message, prefix = '')

    if reaction.message == game.message:
        if reaction.emoji == OPERATOR_ICONS[OperatorIconKeys.DISCUSSION]:
            await open(ctx)
            return
        elif reaction.emoji == OPERATOR_ICONS[OperatorIconKeys.KILL]:
            message = await ctx.send("Who has passed away?")
            for player in game.get_alive_players():
                await message.add_reaction(player.emoji)
            game.kill_message = message
        elif reaction.emoji == OPERATOR_ICONS[OperatorIconKeys.RESET]:
            await reset(ctx)
        elif reaction.emoji == OPERATOR_ICONS[OperatorIconKeys.END]:
            await end(ctx)
            return
    elif reaction.message == game.kill_message:
        for emoji in PLAYER_ICONS:
            if reaction.emoji == emoji:
                await kill(ctx, emoji)
                await game.kill_message.delete()
                game.kill_message = None
                return

    #await reaction.remove(user)

async def on_reaction_remove(reaction: discord.Reaction, user):
    game = games.get(user.voice.channel.id)
    if game is None or reaction.message != game.message:
        return

    ctx = commands.Context(message = game.message, prefix = '')

    if reaction.emoji == OPERATOR_ICONS[OperatorIconKeys.DISCUSSION]:
        await close(ctx)