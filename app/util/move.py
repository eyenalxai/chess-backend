from random import choice, randint

from chess import Board
from stockfish import Stockfish

from app.util.helper import (
    get_move_with_highest_eval,
    get_pieces_under_attack,
    get_time_for_stockfish_strategy,
    parse_move,
    square_color,
)
from app.util.schema import MoveOutcome, StrategyName


def get_stockfish_move(
    *,
    stockfish: Stockfish,
    strategy_name: StrategyName,
    fen_string: str,
) -> MoveOutcome:
    stockfish.set_fen_position(fen_position=fen_string)
    time = get_time_for_stockfish_strategy(strategy=strategy_name)
    best_move = stockfish.get_best_move_time(time=time)

    if not best_move:
        raise Exception("No best move found")

    return parse_move(move=best_move)


def get_random_move(_stockfish: Stockfish, board: Board) -> MoveOutcome:
    return parse_move(move=choice(list(board.generate_legal_moves())).uci())


def get_sidestep_move(
    stockfish: Stockfish,
    board: Board,
) -> MoveOutcome:
    player_color = board.turn
    pieces_under_attack = get_pieces_under_attack(
        board=board,
        player_color=player_color,
    )

    sidestepping_moves = [
        move for move in board.legal_moves if move.from_square in pieces_under_attack
    ]

    if not sidestepping_moves or randint(0, 9) == 0:
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name="stockfish-10",
            fen_string=board.fen(),
        )

    return parse_move(
        move=get_move_with_highest_eval(
            board=board,
            moves=sidestepping_moves,
            player_color=player_color,
        ).uci()
    )


def get_snatcher_move(stockfish: Stockfish, board: Board) -> MoveOutcome:
    capturing_moves = [move for move in board.legal_moves if board.is_capture(move)]

    if not capturing_moves or randint(0, 9) == 0:
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name="stockfish-10",
            fen_string=board.fen(),
        )

    return parse_move(
        move=get_move_with_highest_eval(
            board=board,
            moves=capturing_moves,
            player_color=board.turn,
        ).uci()
    )


def get_chroma_move(stockfish: Stockfish, board: Board) -> MoveOutcome:
    chroma_moves = [
        move
        for move in board.legal_moves
        if square_color(square=move.to_square) != int(board.turn)
    ]

    if not chroma_moves or randint(0, 9) == 0:
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name="stockfish-10",
            fen_string=board.fen(),
        )

    return parse_move(
        move=get_move_with_highest_eval(
            board=board,
            moves=chroma_moves,
            player_color=board.turn,
        ).uci()
    )


def get_contrast_move(stockfish: Stockfish, board: Board) -> MoveOutcome:
    contrast_moves = [
        move
        for move in board.legal_moves
        if square_color(square=move.to_square) == int(board.turn)
    ]

    if not contrast_moves or randint(0, 9) == 0:
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name="stockfish-10",
            fen_string=board.fen(),
        )

    return parse_move(
        move=get_move_with_highest_eval(
            board=board,
            moves=contrast_moves,
            player_color=board.turn,
        ).uci()
    )
