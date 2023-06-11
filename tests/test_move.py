from collections.abc import Callable

from chess import Board, Move, parse_square
from stockfish import Stockfish

from app.util.fish.get_fish import get_stockfish
from app.util.helper import get_piece_type
from app.util.move import (
    get_checkmate_express_move,
    get_dichrome_move,
    get_elusive_move,
    get_monochrome_move,
    get_predator_move,
)
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


def test_get_elusive_move() -> None:
    starting_fen = "k7/8/2q1p1n1/8/B5B1/8/2B5/K7 b - - 0 1"
    ending_fen = "k7/8/4p1n1/8/q5B1/8/2B5/K7 w - - 0 2"

    assert execute_move(
        get_move=get_elusive_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )


def test_get_predator_move() -> None:
    starting_fen = "k7/8/2q1p1n1/8/B5B1/8/2B5/K7 w - - 0 1"
    ending_fen = "k7/8/2B1p1n1/8/6B1/8/2B5/K7 b - - 0 1"

    execute_move(
        get_move=get_predator_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )


def test_get_monochrome_move() -> None:
    starting_fen = "1k6/3n1q2/8/4N3/p1p2p1p/1P4P1/8/1K6 w - - 0 1"
    ending_fen = "1k6/3n1N2/8/8/p1p2p1p/1P4P1/8/1K6 b - - 0 1"

    assert execute_move(
        get_move=get_monochrome_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )


def test_get_dichrome_move() -> None:
    starting_fen = "2kn4/8/2P1N3/5n2/8/1p2R1Q1/R1Q5/5K2 b - - 0 1"
    ending_fen = "2kn4/8/2P1N3/5n2/8/4R1Q1/R1p5/5K2 w - - 0 2"

    assert execute_move(
        get_move=get_dichrome_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )


def test_get_checkmate_express_move() -> None:
    starting_fen = "k7/8/8/8/5p2/8/K3P3/8 w - - 0 1"
    ending_fen = "k7/8/8/8/5p2/4P3/K7/8 b - - 0 1"

    assert execute_move(
        get_move=get_checkmate_express_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )

    starting_fen = "k7/8/8/8/8/6p1/K2Q4/8 w - - 0 1"
    ending_fen = "k7/8/8/8/8/6p1/K6Q/8 b - - 1 1"

    assert execute_move(
        get_move=get_checkmate_express_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )

    starting_fen = "3k4/3n4/1p6/8/2R1P3/6p1/8/K6Q w - - 0 1"
    ending_fen = "3k4/3n4/1p6/8/2R1P3/6p1/7Q/K7 b - - 1 1"

    assert execute_move(
        get_move=get_checkmate_express_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )

    starting_fen = "3k4/3n4/1p6/8/2R1R3/8/8/K7 w - - 0 1"
    ending_fen = "3kR3/3n4/1p6/8/2R5/8/8/K7 b - - 1 1"

    assert execute_move(
        get_move=get_checkmate_express_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )

    starting_fen = "ppP5/kpP1n3/ppP5/PPP5/1p3Q2/5p2/8/K1R3P1 w - - 1 1"
    ending_fen = "ppP5/kpP1n3/ppP5/PPP2Q2/1p6/5p2/8/K1R3P1 b - - 2 1"

    assert execute_move(
        get_move=get_checkmate_express_move,
        starting_fen=starting_fen,
        ending_fen=ending_fen,
    )
