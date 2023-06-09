from random import choice

from chess import Board, WHITE, BLACK
from stockfish import Stockfish

from app.util.helper import (
    is_kamikaze_move,
    is_black_square,
    get_time_for_strategy,
    parse_move,
)
from app.util.schema import MoveOutcome, StrategyName


def get_stockfish_move(
    *,
    stockfish: Stockfish,
    strategy_name: StrategyName,
    fen_string: str,
) -> MoveOutcome:
    stockfish.set_fen_position(fen_position=fen_string)
    time = get_time_for_strategy(strategy=strategy_name)
    best_move = stockfish.get_best_move_time(time=time)

    if not best_move:
        raise Exception("No best move found")

    return parse_move(move=best_move)


def get_random_move(
    *,
    board: Board,
) -> MoveOutcome:
    return parse_move(move=choice(list(board.generate_legal_moves())).uci())


def get_pacifist_move(*, board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())
    pacifist_moves = [move for move in legal_moves if not board.is_capture(move)]

    if not pacifist_moves:
        return get_random_move(board=board)

    return parse_move(move=choice(pacifist_moves).uci())


def get_predator_move(*, board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())
    pacifist_moves = [move for move in legal_moves if board.is_capture(move)]

    if not pacifist_moves:
        return get_random_move(board=board)

    return parse_move(move=choice(pacifist_moves).uci())


def get_pawnstorm_move(*, board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())
    pieces = board.piece_map()

    pawn_squares = [
        square for square, piece in pieces.items() if piece.symbol().lower() == "p"
    ]

    pawn_moves = [move for move in legal_moves if move.from_square in pawn_squares]

    if not pawn_moves:
        return get_random_move(board=board)

    capture_moves = [move for move in pawn_moves if board.is_capture(move)]
    non_capture_moves = [move for move in pawn_moves if not board.is_capture(move)]

    if capture_moves:
        return parse_move(move=choice(capture_moves).uci())

    return parse_move(move=choice(non_capture_moves).uci())


def get_kamikaze_move(*, board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())

    kamikaze_moves = [
        move for move in legal_moves if is_kamikaze_move(board=board, move=move)
    ]

    if kamikaze_moves:
        return parse_move(move=choice(kamikaze_moves).uci())

    return get_pacifist_move(board=board)


def get_same_color_move(*, board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())

    same_color_moves = [
        move
        for move in legal_moves
        if (board.turn == WHITE and not is_black_square(move.to_square))
        or (board.turn == BLACK and is_black_square(move.to_square))
    ]

    if same_color_moves:
        return parse_move(move=choice(same_color_moves).uci())

    return get_random_move(board=board)


def get_opposite_color_move(*, board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())

    opposite_color_moves = [
        move
        for move in legal_moves
        if (board.turn == WHITE and is_black_square(move.to_square))
        or (board.turn == BLACK and not is_black_square(move.to_square))
    ]

    if opposite_color_moves:
        return parse_move(move=choice(opposite_color_moves).uci())

    return get_random_move(board=board)
