from random import random

from chess import PIECE_NAMES, PIECE_SYMBOLS, Board, Move

from app.util.board_evaluation import simulate_move_and_evaluate
from app.util.schema import ChessMove, MoveEvaluation, MoveOutcome, StrategyName


def get_move_with_highest_eval(
    *,
    board: Board,
    moves: list[Move],
    player_color: bool,
) -> Move:
    move_values = [
        MoveEvaluation(
            move=move,
            value=simulate_move_and_evaluate(
                board=board,
                move=move,
                player_color=player_color,
            ),
        )
        for move in moves
    ]
    if not move_values:
        raise Exception("No moves found")

    return max(move_values, key=lambda move_value: move_value.value).move


def parse_move(*, move: str) -> MoveOutcome:
    if len(move) == 4:
        return MoveOutcome(
            chess_move=ChessMove(
                from_square=move[:2],
                to_square=move[2:],
            )
        )

    if len(move) == 5:
        return MoveOutcome(
            chess_move=ChessMove(
                from_square=move[:2],
                to_square=move[2:4],
                promotion=move[4],
            )
        )

    raise Exception("Invalid best move")


def get_time_for_stockfish_strategy(*, strategy: StrategyName) -> int:
    if strategy == "stockfish-1":
        return 1
    if strategy == "stockfish-10":
        return 10
    if strategy == "stockfish-100":
        return 100
    if strategy == "stockfish-500":
        return 500
    if strategy == "stockfish-1000":
        return 1000

    raise Exception("Invalid strategy")


def get_piece_type(*, name: str | None) -> int | None:
    if name is None:
        return None
    if name in PIECE_SYMBOLS:
        return PIECE_SYMBOLS.index(name)
    if name in PIECE_NAMES:
        return PIECE_NAMES.index(name)
    return None


def is_probability_proc(
    *,
    probability: float,
) -> bool:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("Probability must be between 0 and 1")

    return random() < probability


def should_do_stockfish_move(
    *,
    moves: list[Move],
    stockfish_move_prob: float,
) -> bool:
    return not moves or is_probability_proc(probability=stockfish_move_prob)
