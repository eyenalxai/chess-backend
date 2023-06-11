from collections.abc import Callable

from chess import Board, Move, parse_square
from stockfish import Stockfish

from app.util.fish import get_stockfish
from app.util.helper import get_piece_type
from app.util.move import get_chroma_move, get_sidestep_move, get_snatcher_move
from app.util.schema import MoveOutcome


def execute_move(
    get_move: Callable[[Stockfish, Board, float], MoveOutcome],
    starting_fen: str,
    ending_fen: str,
) -> bool:
    board = Board(fen=starting_fen)
    stockfish = get_stockfish()
    stockfish_move_prob = 0

    move = get_move(stockfish, board, stockfish_move_prob)

    if not move.chess_move:
        raise Exception("No best move found")

    board.push(
        move=Move(
            from_square=parse_square(name=move.chess_move.from_square),
            to_square=parse_square(name=move.chess_move.to_square),
            promotion=get_piece_type(name=move.chess_move.promotion),
        )
    )

    current_fen = board.fen()
    if current_fen != ending_fen:
        print(f"Board FEN: {current_fen}")

    return current_fen == ending_fen


def test_get_sidestep_move() -> None:
    starting_fen = "k7/8/2q1p1n1/8/B5B1/8/2B5/K7 b - - 0 1"
    ending_fen = "k7/8/4p1n1/8/q5B1/8/2B5/K7 w - - 0 2"

    assert execute_move(
        get_move=get_sidestep_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )


def test_get_snatcher_move() -> None:
    starting_fen = "k7/8/2q1p1n1/8/B5B1/8/2B5/K7 w - - 0 1"
    ending_fen = "k7/8/2B1p1n1/8/6B1/8/2B5/K7 b - - 0 1"

    execute_move(
        get_move=get_snatcher_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )


def test_get_chroma_move() -> None:
    starting_fen = "1k6/3n1q2/8/4N3/p1p2p1p/1P4P1/8/1K6 w - - 0 1"
    ending_fen = "1k6/3n1N2/8/8/p1p2p1p/1P4P1/8/1K6 b - - 0 1"

    assert execute_move(
        get_move=get_chroma_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )
