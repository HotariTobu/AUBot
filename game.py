from enum import Enum, auto

class GameState(Enum):
    MENDING = auto(),
    DISCUSSING = auto(),

class Game:
    def __init__(self, players, message):
        self.state = GameState.MENDING
        self.players = players
        self.message = message

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
        return False

    async def reset(self):
        self.state = GameState.MENDING
        for player in self.players:
            player.is_killed = False
            await player.member.edit(
                mute = False,
                deafen = False
            )

    def get_alive_players(self) -> list:
        return [player for player in self.players if not player.is_killed]