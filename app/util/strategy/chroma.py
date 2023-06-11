from chess import Board, Move

from app.util.board_evaluation import get_square_color


def is_move_from_opposite_color_to_same_color(*, board: Board, move: Move) -> bool:
    return (
        get_square_color(square=move.from_square) != board.turn
        and get_square_color(square=move.to_square) == board.turn
    )


def filter_moves_from_opposite_color_to_same_color(
    board: Board,
    moves: list[Move],
) -> list[Move]:
    return [
        move
        for move in moves
        if is_move_from_opposite_color_to_same_color(board=board, move=move)
    ]


def is_move_from_same_color_to_same_color(*, board: Board, move: Move) -> bool:
    return (
        get_square_color(square=move.from_square) == board.turn
        and get_square_color(square=move.to_square) == board.turn
    )


def filter_moves_from_same_color_to_same_color(
    board: Board,
    moves: list[Move],
) -> list[Move]:
    return [
        move
        for move in moves
        if is_move_from_same_color_to_same_color(board=board, move=move)
    ]
