import discord
from discord.ext import commands

from icon import OperatorIconKeys, OPERATOR_ICONS, PLAYER_ICONS
from game import Game
import text

games = {}

def get_id_from(ctx: commands.Context):
    return ctx.author.voice.channel.id

async def begin(ctx: commands.Context):
    if ctx.author.voice is None:
        await ctx.send(text.NONE_VOICE_TEXT)
        return

    if get_id_from(ctx) in games:
        await ctx.send(text.BEGUN_GAME_TEXT)
        return
    
    message = await ctx.send(text.get_game_text(ctx.author.voice.channel.name))
    game = Game(message, ctx.author.voice.channel)
    games[get_id_from(ctx)] = game
    
    await game.update_embed()
    for key in OperatorIconKeys:
        await message.add_reaction(OPERATOR_ICONS[key])

async def open(ctx: commands.Context):
    game = games.get(get_id_from(ctx))
    if game is None:
        await ctx.send(text.FAILED_TEXT)
        return

    await game.open()

async def close(ctx: commands.Context):
    game = games.get(get_id_from(ctx))
    if game is None:
        await ctx.send(text.FAILED_TEXT)
        return

    await game.close()

async def kill(ctx: commands.Context, arg: str):
    game = games.get(get_id_from(ctx))
    if game is None:
        await ctx.send(text.FAILED_TEXT)
        return
        
    if (await game.kill(arg)):
        await ctx.send(text.get_failed_kill_text(arg))

async def reset(ctx: commands.Context):
    game = games.get(get_id_from(ctx))
    if game is None:
        await ctx.send(text.FAILED_TEXT)
        return

    await game.reset()

async def end(ctx: commands.Context):
    game = games.pop(get_id_from(ctx), None)
    if game is None:
        await ctx.send(text.FAILED_TEXT)
        return

    await game.end()

async def on_reaction_add(reaction: discord.Reaction, user):
    if user.voice is None:
        return
    
    game = games.get(user.voice.channel.id)
    if game is None:
        return

    if reaction.message == game.message:
        if reaction.emoji == OPERATOR_ICONS[OperatorIconKeys.DISCUSSION]:
            await game.open()
            return
        elif reaction.emoji == OPERATOR_ICONS[OperatorIconKeys.KILL]:
            alive_players = game.get_alive_players()
            if len(alive_players) > 0:
                message = await reaction.message.channel.send(text.KILL_TEXT)
                for player in alive_players:
                    await message.add_reaction(player.emoji)
                game.kill_message = message
        elif reaction.emoji == OPERATOR_ICONS[OperatorIconKeys.RESET]:
            await game.reset()
        elif reaction.emoji == OPERATOR_ICONS[OperatorIconKeys.END]:
            del games[user.voice.channel.id]
            await game.end()
            return
    elif reaction.message == game.kill_message:
        for emoji in PLAYER_ICONS:
            if reaction.emoji == emoji:
                await game.kill(emoji)
                await game.kill_message.delete()
                game.kill_message = None
                return

    #await reaction.remove(user)

async def on_reaction_remove(reaction: discord.Reaction, user):
    if user.voice is None:
        return
    
    game = games.get(user.voice.channel.id)
    if game is None or reaction.message != game.message:
        return

    if reaction.emoji == OPERATOR_ICONS[OperatorIconKeys.DISCUSSION]:
        await game.close()

async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if (before.channel is None):
        return
    
    game = games.get(before.channel.id)
    if game is None:
        return

    if len(before.channel.members) == 0:
        del games[before.channel.id]
        await game.end()