from discord import Member

class Player:
    def __init__(self, emoji: str, member: Member) -> None:
        self.emoji = emoji
        self.member = member
        self.name = member.name if member.nick is None else member.nick
        self.is_killed = False