from random import random
from typing import NamedTuple

from chess import (
    PIECE_NAMES,
    PIECE_SYMBOLS,
    SQUARES,
    Board,
    Move,
    Outcome,
    Piece,
    Square,
    Termination,
    square_file,
    square_rank,
)

from app.util.schema import (
    ChessMove,
    GameOutcome,
    MoveOutcome,
    Reason,
    StrategyName,
    Winner,
)

TERMINATION_REASON: dict[Termination, Reason] = {
    Termination.CHECKMATE: "checkmate",
    Termination.STALEMATE: "stalemate",
    Termination.INSUFFICIENT_MATERIAL: "insufficient_material",
    Termination.SEVENTYFIVE_MOVES: "seventyfive_moves",
    Termination.FIVEFOLD_REPETITION: "fivefold_repetition",
    Termination.FIFTY_MOVES: "fifty_moves",
    Termination.THREEFOLD_REPETITION: "threefold_repetition",
    Termination.VARIANT_WIN: "variant_win",
    Termination.VARIANT_LOSS: "variant_loss",
    Termination.VARIANT_DRAW: "variant_draw",
}

PIECE_VALUES = {None: 0, "p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 100}


def get_piece_value(*, piece: Piece) -> int:
    piece_symbol = piece.symbol().lower()

    if piece_symbol in PIECE_SYMBOLS:
        return PIECE_VALUES[piece_symbol]

    raise Exception("Invalid piece")


def get_piece_value_for_player(*, piece: Piece, player_color: bool) -> int:
    piece_symbol = piece.symbol().lower()

    if piece_symbol in PIECE_SYMBOLS:
        if piece.color == player_color:
            return get_piece_value(piece=piece)

        return -get_piece_value(piece=piece)

    raise Exception("Invalid piece")


def evaluate_board(*, board: Board, player_color: bool) -> int:
    value = 0

    for square in range(64):
        piece = board.piece_at(square=square)

        if piece is not None:
            value += get_piece_value_for_player(piece=piece, player_color=player_color)

    return value


def simulate_move_and_evaluate(*, board: Board, move: Move, player_color: bool) -> int:
    hypothetical_board = board.copy(stack=False)
    hypothetical_board.push(move=move)
    return evaluate_board(board=hypothetical_board, player_color=player_color)


class MoveEvaluation(NamedTuple):
    move: Move
    value: int


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

    return max(move_values, key=lambda move_value: move_value.value).move


def is_square_under_attack(*, board: Board, square: int, player_color: bool) -> bool:
    return board.is_attacked_by(color=not player_color, square=square)


def is_piece_on_square_of_player_color(
    *, board: Board, square: int, player_color: bool
) -> bool:
    piece = board.piece_at(square=square)
    return piece is not None and piece.color == player_color


def get_pieces_under_attack(*, board: Board, player_color: bool) -> list[int]:
    return [
        square
        for square in SQUARES
        if is_square_under_attack(board=board, square=square, player_color=player_color)
        and is_piece_on_square_of_player_color(
            board=board,
            square=square,
            player_color=player_color,
        )
    ]


def get_game_outcome(*, board: Board) -> MoveOutcome | None:
    if board.is_game_over():
        outcome = board.outcome()
        if outcome is not None:
            winner = get_winner(outcome=outcome)
            reason = TERMINATION_REASON.get(outcome.termination)
            if reason is not None:
                return MoveOutcome(
                    game_outcome=GameOutcome(
                        winner=winner,
                        reason=reason,
                    )
                )
            raise Exception("Invalid reason")
        raise Exception("Invalid outcome")

    return None


def get_winner(*, outcome: Outcome) -> Winner:
    if outcome.winner is None:
        return "draw"

    if outcome.winner:
        return "white"

    return "black"


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


def get_time_for_stockfish_strategy(strategy: StrategyName) -> int:
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


def get_piece_type(name: str | None) -> int | None:
    if name is None:
        return None
    if name in PIECE_SYMBOLS:
        return PIECE_SYMBOLS.index(name)
    if name in PIECE_NAMES:
        return PIECE_NAMES.index(name)
    return None


def count_opponent_pieces(*, board: Board, player_color: bool) -> int:
    opponent_color = not player_color
    return sum(
        1
        for square in SQUARES
        if (piece := board.piece_at(square)) and piece.color == opponent_color
    )


def square_color(square: Square) -> int:
    file = square_file(square)
    rank = square_rank(square)
    return (rank + file) % 2


def is_probability_proc(
    *,
    probability: float,
) -> bool:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("Probability must be between 0 and 1")

    return random() < probability


def should_do_stockfish(
    moves: list[Move],
    stockfish_move_prob: float,
) -> bool:
    return not moves or is_probability_proc(probability=stockfish_move_prob)
