from random import choice, shuffle

from chess import Board, WHITE, BLACK, square_mirror, square_distance, SQUARES
from stockfish import Stockfish

from app.util.helper import (
    is_black_square,
    get_time_for_strategy,
    parse_move,
    is_kamikaze_move,
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


def get_pacifist_move(board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())
    pacifist_moves = [move for move in legal_moves if not board.is_capture(move=move)]

    if not pacifist_moves:
        return get_random_move(board=board)

    return parse_move(move=choice(pacifist_moves).uci())


def get_predator_move(board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())
    pacifist_moves = [move for move in legal_moves if board.is_capture(move=move)]

    if not pacifist_moves:
        return get_random_move(board=board)

    return parse_move(move=choice(pacifist_moves).uci())


def get_pawnstorm_move(board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())
    pieces = board.piece_map()

    pawn_squares = [
        square for square, piece in pieces.items() if piece.symbol().lower() == "p"
    ]

    pawn_moves = [move for move in legal_moves if move.from_square in pawn_squares]

    if not pawn_moves:
        return get_random_move(board=board)

    capture_moves = [move for move in pawn_moves if board.is_capture(move=move)]
    non_capture_moves = [move for move in pawn_moves if not board.is_capture(move=move)]

    if capture_moves:
        return parse_move(move=choice(capture_moves).uci())

    return parse_move(move=choice(non_capture_moves).uci())


def get_kamikaze_move(board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())

    kamikaze_moves = [
        move for move in legal_moves if is_kamikaze_move(board=board, move=move)
    ]

    if kamikaze_moves:
        return parse_move(move=choice(kamikaze_moves).uci())

    return get_predator_move(board=board)


def get_chroma_move(board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())

    same_color_moves = [
        move
        for move in legal_moves
        if (board.turn == WHITE and not is_black_square(square=move.to_square))
        or (board.turn == BLACK and is_black_square(square=move.to_square))
    ]

    if same_color_moves:
        return parse_move(move=choice(same_color_moves).uci())

    return get_random_move(board=board)


def get_contrast_move(board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())

    opposite_color_moves = [
        move
        for move in legal_moves
        if (board.turn == WHITE and is_black_square(square=move.to_square))
        or (board.turn == BLACK and not is_black_square(square=move.to_square))
    ]

    if opposite_color_moves:
        return parse_move(move=choice(opposite_color_moves).uci())

    return get_random_move(board=board)


def get_mirror_move(board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())
    pieces = board.piece_map()

    current_player_pieces = {
        sq: piece for sq, piece in pieces.items() if piece.color == board.turn
    }

    piece_mirror_positions = {
        sq: square_mirror(sq) for sq in current_player_pieces.keys()
    }

    piece_keys = list(current_player_pieces.keys())
    shuffle(piece_keys)

    for piece_key in piece_keys:
        current_piece_moves = [
            move for move in legal_moves if move.from_square == piece_key
        ]

        if current_piece_moves:
            best_move = min(
                current_piece_moves,
                key=lambda move: square_distance(
                    move.to_square, piece_mirror_positions[move.from_square]
                ),
            )
            return parse_move(move=best_move.uci())

    return get_random_move(board=board)


def get_fortify_move(board: Board) -> MoveOutcome:
    current_player_color = board.turn

    pieces_under_attack = [
        square
        for square in SQUARES
        if board.is_attacked_by(not current_player_color, square)
        and board.piece_at(square)
        and board.piece_at(square).color == current_player_color
    ]

    min_attackers = float("inf")
    safest_move = None

    for square in pieces_under_attack:
        legal_moves = board.legal_moves
        piece_moves = [move for move in legal_moves if move.from_square == square]

        for move in piece_moves:
            hypothetical_board = board.copy()
            hypothetical_board.push(move)

            num_attackers = len(
                hypothetical_board.attackers(
                    color=not current_player_color, square=move.to_square
                )
            )

            if num_attackers < min_attackers:
                min_attackers = num_attackers
                safest_move = move

    if safest_move is not None:
        return parse_move(move=safest_move.uci())

    return get_random_move(board=board)
