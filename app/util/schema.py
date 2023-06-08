from typing import Literal

from app.config.pydantic import Immutable

StrategyName = Literal[
    "random",
    "pacifist",
    "stockfish-100",
    "stockfish-500",
    "stockfish-1000",
]


class MoveRequest(Immutable):
    fen_string: str
    strategy_name: StrategyName


Winner = Literal["white", "black", "draw"]

Reason = Literal[
    "checkmate",
    "stalemate",
    "insufficient_material",
    "seventyfive_moves",
    "fivefold_repetition",
    "fifty_moves",
    "threefold_repetition",
    "variant_win",
    "variant_loss",
    "variant_draw",
]


class GameOutcome(Immutable):
    winner: Winner
    reason: Reason
    ended: bool


class ChessMove(Immutable):
    from_square: str | None = None
    to_square: str | None = None
    promotion: str | None = None
    game_outcome: GameOutcome | None = None
