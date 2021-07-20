from enum import Enum, auto
import discord

from icon import PLAYER_ICONS
from player import Player
import text

class GameState(Enum):
    MENDING = auto(),
    DISCUSSING = auto(),

class Game:
    async def update_embed(self):
        description = ""
        for player in self.players:
            if player.is_killed:
                description += f"||{player.emoji}:\t{player.name}||\n"
            else:
                description += f"{player.emoji}:\t{player.name}\n"
        description += f"\n{text.OPERATOR_ICONS_STR}"

        embed = discord.Embed(description = description)
        await self.message.edit(embed = embed)

    def update_players(self) -> list:
        self.players = [Player(PLAYER_ICONS[index], member) for index, member in enumerate([member for member in self.channel.members if not member.bot])]

    def __init__(self, message: discord.Message, channel):
        self.state = GameState.MENDING
        self.message = message
        self.kill_message = None
        self.channel = channel
        self.update_players()

    async def update_player_state(self, player):
        await player.member.edit(
            mute = (True if self.state == GameState.MENDING else False) if not player.is_killed else (False if self.state == GameState.MENDING else True),
            deafen = False if player.is_killed else (True if self.state == GameState.MENDING else False)
        )

    async def open(self):
        self.state = GameState.DISCUSSING
        for player in self.players:
            await self.update_player_state(player)

    async def close(self):
        self.state = GameState.MENDING
        for player in self.players:
            await self.update_player_state(player)

    async def kill(self, arg: str) -> bool:
        dead = None

        if arg.isdecimal():
            number = int(arg)
            if number < len(self.players) and number >= 0:
                dead = self.players[number]
            else:
                for player in self.players:
                    if player.member.id == number:
                        dead = player
                        break;
        else:
            for player in self.players:
                if arg in [player.emoji, player.member.nick, player.member.name]:
                    dead = player
                    break;

        if dead is None:
            return True
            
        dead.is_killed = True
        await self.update_player_state(dead)
        await self.update_embed()
        return False

    async def reset_players(self):
        for player in self.players:
            if not player.member.voice is None:
                player.is_killed = False
                await player.member.edit(
                    mute = False,
                    deafen = False
                )

    async def reset(self):
        self.state = GameState.MENDING
        await self.reset_players()
        self.update_players()
        await self.update_embed()
        if (not self.kill_message is None):
            await self.kill_message.delete()

    async def end(self):
        await self.reset_players()
        await self.message.delete()
        if (not self.kill_message is None):
            await self.kill_message.delete()

    def get_alive_players(self) -> list:
        return [player for player in self.players if not player.is_killed]