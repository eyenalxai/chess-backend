from collections.abc import Callable

from chess import (
    BLACK,
    PIECE_SYMBOLS,
    SQUARES,
    WHITE,
    Board,
    Color,
    Move,
    Piece,
    Square,
    square_file,
    square_rank,
)

from app.util.schema import MoveEvaluation

PIECE_VALUES = {None: 0, "p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 100}


def get_piece_value(*, piece: Piece) -> int:
    piece_symbol = piece.symbol().lower()

    if piece_symbol in PIECE_SYMBOLS:
        return PIECE_VALUES[piece_symbol]

    raise Exception("Invalid piece")


def get_piece_value_for_player(*, piece: Piece, player_color: Color) -> int:
    piece_symbol = piece.symbol().lower()

    if piece_symbol in PIECE_SYMBOLS:
        if piece.color == player_color:
            return get_piece_value(piece=piece)

        return -get_piece_value(piece=piece)

    raise Exception("Invalid piece")


def evaluate_board(*, board: Board, player_color: Color) -> int:
    value = 0

    for square in range(64):
        piece = board.piece_at(square=square)

        if piece is not None:
            value += get_piece_value_for_player(piece=piece, player_color=player_color)

    return value


def simulate_move_and_evaluate(*, board: Board, move: Move) -> int:
    hypothetical_board = board.copy(stack=False)
    hypothetical_board.push(move=move)
    return evaluate_board(board=hypothetical_board, player_color=board.turn)


def is_square_under_attack(*, board: Board, square: int, player_color: bool) -> bool:
    return board.is_attacked_by(color=not player_color, square=square)


def get_pieces_under_attack(*, board: Board, player_color: bool) -> list[int]:
    return [
        square
        for square in SQUARES
        if is_square_under_attack(board=board, square=square, player_color=player_color)
        and is_players_piece_on_square(
            board=board,
            square=square,
            player_color=player_color,
        )
    ]


def count_opponent_pieces(*, board: Board, player_color: Color) -> int:
    return sum(
        1
        for square in SQUARES
        if (piece := board.piece_at(square=square)) and piece.color != player_color
    )


def is_white_square(*, square: Square) -> bool:
    return (square_file(square) + square_rank(square)) % 2 != 0


def is_black_square(*, square: Square) -> bool:
    return not is_white_square(square=square)


def get_square_color(*, square: Square) -> Color:
    return WHITE if is_white_square(square=square) else BLACK


def is_players_piece_on_square(
    *, board: Board, square: int, player_color: bool
) -> bool:
    piece = board.piece_at(square=square)
    return piece is not None and piece.color == player_color


def get_move_based_on_value(*, move_values: list[MoveEvaluation], fn: Callable) -> Move:
    return fn(move_values, key=lambda move_value: move_value.value).move


class NoMovesToEvaluateError(Exception):
    """Raised when there are no moves to evaluate"""

    pass


def evaluate_and_get_optimal_move(
    *,
    board: Board,
    moves: list[Move],
    is_max: bool = True,
) -> Move:
    move_values = [
        MoveEvaluation(
            move=move,
            value=simulate_move_and_evaluate(
                board=board,
                move=move,
            ),
        )
        for move in moves
    ]
    if not move_values:
        raise NoMovesToEvaluateError

    fn = max if is_max else min
    return get_move_based_on_value(move_values=move_values, fn=fn)
