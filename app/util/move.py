from collections.abc import Callable
from random import choice

from chess import Board, Move
from stockfish import Stockfish

from app.util.board_evaluation import get_pieces_under_attack
from app.util.helper import (
    get_move_with_highest_eval,
    get_time_for_stockfish_strategy,
    is_probability_proc,
    parse_move,
    should_do_stockfish_move,
)
from app.util.schema import MoveOutcome, StrategyName
from app.util.strategy.chroma import (
    filter_moves_from_opposite_color_to_same_color,
    filter_moves_from_same_color_to_same_color,
)
from app.util.strategy.contrast import (
    filter_moves_from_opposite_color_to_opposite_color,
    filter_moves_from_same_color_to_opposite_color,
)


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


def get_random_move(
    _stockfish: Stockfish,
    board: Board,
    _stockfish_move_prob: float,
) -> MoveOutcome:
    return parse_move(move=choice(list(board.generate_legal_moves())).uci())


def get_sidestep_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float = 0.1,
) -> MoveOutcome:
    player_color = board.turn
    pieces_under_attack = get_pieces_under_attack(
        board=board,
        player_color=player_color,
    )

    sidestepping_moves = [
        move for move in board.legal_moves if move.from_square in pieces_under_attack
    ]

    if should_do_stockfish_move(
        moves=sidestepping_moves,
        stockfish_move_prob=stockfish_move_prob,
    ):
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


def get_snatcher_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
) -> MoveOutcome:
    capturing_moves = [move for move in board.legal_moves if board.is_capture(move)]

    if should_do_stockfish_move(
        moves=capturing_moves,
        stockfish_move_prob=stockfish_move_prob,
    ):
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


def get_chroma_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
) -> MoveOutcome:
    return get_best_move_after_filtering(
        stockfish=stockfish,
        board=board,
        stockfish_move_prob=stockfish_move_prob,
        filter_functions=[
            filter_moves_from_opposite_color_to_same_color,
            filter_moves_from_same_color_to_same_color,
        ],
    )


def get_contrast_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
) -> MoveOutcome:
    return get_best_move_after_filtering(
        stockfish=stockfish,
        board=board,
        stockfish_move_prob=stockfish_move_prob,
        filter_functions=[
            filter_moves_from_same_color_to_opposite_color,
            filter_moves_from_opposite_color_to_opposite_color,
        ],
    )


def get_best_move_after_filtering(
    *,
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
    filter_functions: list[Callable[[Board, list[Move]], list[Move]]],
) -> MoveOutcome:
    if is_probability_proc(probability=stockfish_move_prob):
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name="stockfish-10",
            fen_string=board.fen(),
        )

    for filter_function in filter_functions:
        filtered_moves = filter_function(board, list(board.legal_moves))
        if filtered_moves:
            return parse_move(
                move=get_move_with_highest_eval(
                    board=board,
                    moves=filtered_moves,
                    player_color=board.turn,
                ).uci()
            )

    return get_stockfish_move(
        stockfish=stockfish,
        strategy_name="stockfish-10",
        fen_string=board.fen(),
    )
