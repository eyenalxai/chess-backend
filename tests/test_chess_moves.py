from chess import Board, Move, parse_square

from app.util.helper import get_piece_type
from app.util.strategy import get_predator_move


def test_get_predator_move() -> None:
    starting_fen = "rnb1k1n1/ppp1pppp/8/4q1b1/3p3r/5N2/PPPPPPPP/RNBQKB1R w KQq - 0 1"
    ending_fen = "rnb1k1n1/ppp1pppp/8/4N1b1/3p3r/8/PPPPPPPP/RNBQKB1R b KQq - 0 1"

    board = Board(fen=starting_fen)
    predator_move = get_predator_move(board=board)

    if not predator_move.chess_move:
        raise Exception("No best move found")

    board.push(
        move=Move(
            from_square=parse_square(name=predator_move.chess_move.from_square),
            to_square=parse_square(name=predator_move.chess_move.to_square),
            promotion=get_piece_type(name=predator_move.chess_move.promotion),
        )
    )

    assert board.fen() == ending_fen
