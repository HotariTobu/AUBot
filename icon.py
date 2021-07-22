from enum import Enum, auto

class OperatorIconKeys(Enum):
    DISCUSSION = auto(),
    KILL = auto(),
    RESET = auto(),
    END = auto(),

OPERATOR_ICONS = {
    OperatorIconKeys.DISCUSSION: '💬',
    OperatorIconKeys.KILL: '🔫',
    OperatorIconKeys.RESET: '🔄',
    OperatorIconKeys.END: '🚪',
}

PLAYER_ICONS = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐸', '🐵', '🐔', '🐧', '🐦', '🐤', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', ]