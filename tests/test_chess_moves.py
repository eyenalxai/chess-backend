from collections.abc import Callable

from chess import Board, Move, parse_square

from app.util.helper import get_piece_type
from app.util.move import get_fortify_move, get_predator_move
from app.util.schema import MoveOutcome


def execute_move(
    get_move: Callable[[Board], MoveOutcome],
    starting_fen: str,
    ending_fen: str,
) -> bool:
    board = Board(fen=starting_fen)
    move = get_move(board)

    if not move.chess_move:
        raise Exception("No best move found")

    board.push(
        move=Move(
            from_square=parse_square(name=move.chess_move.from_square),
            to_square=parse_square(name=move.chess_move.to_square),
            promotion=get_piece_type(name=move.chess_move.promotion),
        )
    )

    return board.fen() == ending_fen


def test_get_predator_move() -> None:
    starting_fen = "rnb1k1n1/ppp1pppp/8/4q1b1/3p3r/5N2/PPPPPPPP/RNBQKB1R w KQq - 0 1"
    ending_fen = "rnb1k1n1/ppp1pppp/8/4N1b1/3p3r/8/PPPPPPPP/RNBQKB1R b KQq - 0 1"

    assert execute_move(get_predator_move, starting_fen, ending_fen)


def test_get_fortify_move() -> None:
    starting_fen = "4k3/8/5q2/r3P2b/P2P3P/n7/8/1P3K2 w - - 0 1"
    ending_fen = "4k3/8/5P2/r6b/P2P3P/n7/8/1P3K2 b - - 0 1"

    assert execute_move(get_fortify_move, starting_fen, ending_fen)
