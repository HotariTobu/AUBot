from icon import OperatorIconKeys, OPERATOR_ICONS

PREFIXES = ['au', 'Au']

HELP_TEXT = f"""\
To play, first, gather members in a voice channel, and then call beginning command.
When someone passed away, call killing command.
A prefix is needed to call commands.
Prefixes:
    {", ".join(PREFIXES)}
Commands:
    b, begin:\tbegin the game
    o, open:\topen a discussion
    c, close:\tclose the discussion
    k, kill N:\tkill N
    r, reset:\treset the game
    e, end:\tend the game"""

NONE_VOICE_TEXT = "You are not connected to any voice channel."
BEGUN_GAME_TEXT = "The game has already begun!"
def get_game_text(arg: str):
    return f"Let's enjoy! - {arg} -"
def get_embed_text(arg: int):
    return f"{arg} players\n"

FAILED_TEXT = "Pls. begin a game before calling some commands."

KILL_TEXT = "Who has passed away?"
KILL_COMMAND_TEXT = "Index, emoji, name, or nickname is needed in the back of the command."
def get_failed_kill_text(arg: str):
    return f"There is no player tagged or named {arg}"

OPERATOR_ICONS_STR = f"""\
{OPERATOR_ICONS[OperatorIconKeys.DISCUSSION]}:\tswitch discussion
{OPERATOR_ICONS[OperatorIconKeys.KILL]}:\tkill N
{OPERATOR_ICONS[OperatorIconKeys.RESET]}:\treset the game
{OPERATOR_ICONS[OperatorIconKeys.END]}:\tend the game
"""