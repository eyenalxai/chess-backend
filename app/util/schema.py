from typing import Literal, NamedTuple

from chess import Move

from app.config.pydantic import Immutable

StrategyName = Literal[
    "random-move",
    "elusive",
    "predator",
    "monochrome",
    "dichrome",
    "checkmate-express",
    "random-strategy",
    "stockfish",
    "stockfish-1",
    "stockfish-10",
    "stockfish-100",
    "stockfish-500",
    "stockfish-1000",
]


class StrategyRequest(Immutable):
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


class ChessMove(Immutable):
    from_square: str
    to_square: str
    promotion: str | None = None


class MoveOutcome(Immutable):
    chess_move: ChessMove | None = None
    game_outcome: GameOutcome | None = None


class MoveEvaluation(NamedTuple):
    move: Move
    value: int
