from chess import BLACK, SQUARES, WHITE, Board, Move

from app.util.board_evaluation import get_square_color, is_black_square, is_white_square
from app.util.strategy.chroma import (
    is_move_from_opposite_color_to_same_color,
    is_move_from_same_color_to_same_color,
)
from app.util.strategy.contrast import (
    is_move_from_opposite_color_to_opposite_color,
    is_move_from_same_color_to_opposite_color,
)


def test_square_color() -> None:
    black_colors = [
        get_square_color(square=square)
        for square in SQUARES
        if is_black_square(square=square)
    ]

    white_colors = [
        get_square_color(square=square)
        for square in SQUARES
        if is_white_square(square=square)
    ]

    assert len(black_colors) == 32
    assert black_colors == [BLACK] * 32

    assert len(white_colors) == 32
    assert white_colors == [WHITE] * 32


def test_is_move_from_opposite_color_to_same_color() -> None:
    board = Board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move = Move.from_uci("f2f3")

    assert is_move_from_opposite_color_to_same_color(board=board, move=move)

    board = Board(fen="rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq - 0 1")
    move = Move.from_uci("b7b6")

    assert is_move_from_opposite_color_to_same_color(board=board, move=move) is True


def test_is_move_from_same_color_to_same_color() -> None:
    board = Board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move = Move.from_uci("e2e4")

    assert is_move_from_same_color_to_same_color(board=board, move=move)

    board = Board(fen="rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq - 0 1")
    move = Move.from_uci("c7c5")

    assert is_move_from_same_color_to_same_color(board=board, move=move)


def test_is_move_from_same_color_to_opposite_color() -> None:
    board = Board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move = Move.from_uci("e2e3")

    assert is_move_from_same_color_to_opposite_color(board=board, move=move)

    board = Board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
    move = Move.from_uci("c7c6")

    assert is_move_from_same_color_to_opposite_color(board=board, move=move)


def test_is_move_from_opposite_color_to_opposite_color() -> None:
    board = Board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move = Move.from_uci("b2b4")

    assert is_move_from_opposite_color_to_opposite_color(board=board, move=move)

    board = Board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
    move = Move.from_uci("d7d5")

    assert is_move_from_opposite_color_to_opposite_color(board=board, move=move)
