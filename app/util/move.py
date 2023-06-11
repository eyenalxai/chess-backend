from collections.abc import Callable
from random import choice
from typing import cast

from chess import Board, Move
from stockfish import Stockfish

from app.util.board_evaluation import (
    evaluate_and_get_optimal_move,
    get_move_based_on_value,
)
from app.util.helper import (
    get_time_for_stockfish_strategy,
    parse_move,
    should_do_stockfish_move,
)
from app.util.schema import MoveOutcome, StrategyName
from app.util.strategy.checkmate_express import get_worst_moves
from app.util.strategy.dichrome import filter_dichrome_moves
from app.util.strategy.elusive import filter_elusive_moves
from app.util.strategy.monochrome import filter_monochrome_moves
from app.util.strategy.predator import filter_predator_moves


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

    return parse_move(move_uci=best_move)


def get_random_move(
    _stockfish: Stockfish,
    board: Board,
    _stockfish_move_prob: float,
) -> MoveOutcome:
    return parse_move(move_uci=choice(list(board.generate_legal_moves())).uci())


def get_move(
    *,
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
    filter_moves: Callable[[Board], list[Move]],
) -> MoveOutcome:
    filtered_moves = filter_moves(board)

    if should_do_stockfish_move(
        moves=filtered_moves,
        stockfish_move_prob=stockfish_move_prob,
    ):
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name="stockfish-10",
            fen_string=board.fen(),
        )

    return parse_move(
        move_uci=evaluate_and_get_optimal_move(
            board=board,
            moves=filtered_moves,
        ).uci()
    )


def get_elusive_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float = 0.1,
) -> MoveOutcome:
    return get_move(
        stockfish=stockfish,
        board=board,
        stockfish_move_prob=stockfish_move_prob,
        filter_moves=filter_elusive_moves,
    )


def get_predator_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
) -> MoveOutcome:
    return get_move(
        stockfish=stockfish,
        board=board,
        stockfish_move_prob=stockfish_move_prob,
        filter_moves=filter_predator_moves,
    )


def get_monochrome_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
) -> MoveOutcome:
    return get_move(
        stockfish=stockfish,
        board=board,
        stockfish_move_prob=stockfish_move_prob,
        filter_moves=filter_monochrome_moves,
    )


def get_dichrome_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
) -> MoveOutcome:
    return get_move(
        stockfish=stockfish,
        board=board,
        stockfish_move_prob=stockfish_move_prob,
        filter_moves=filter_dichrome_moves,
    )


def get_checkmate_express_move(
    _stockfish: Stockfish,
    board: Board,
    _stockfish_move_prob: float,
) -> MoveOutcome:
    worst_moves = get_worst_moves(board=board, player_moves=list(board.legal_moves))

    if worst_moves:
        # Max is because we calculate the worst moves
        # based on the opponent's perspective
        move = get_move_based_on_value(move_values=worst_moves, fn=max)
        return parse_move(move_uci=move.uci())

    return get_random_move(
        _stockfish=_stockfish,
        board=board,
        _stockfish_move_prob=_stockfish_move_prob,
    )


def get_random_strategy_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
) -> MoveOutcome:
    strategies: list[StrategyName] = [
        "random-move",
        "elusive",
        "predator",
        "monochrome",
        "dichrome",
        "checkmate-express",
        "stockfish",
    ]

    strategy = choice(strategies)

    if strategy == "stockfish":
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name=cast(
                StrategyName,
                choice(
                    [
                        "stockfish-1",
                        "stockfish-10",
                        "stockfish-100",
                        "stockfish-500",
                        "stockfish-1000",
                    ]
                ),
            ),
            fen_string=board.fen(),
        )

    if strategy == "random-move":
        return get_random_move(
            _stockfish=stockfish,
            board=board,
            _stockfish_move_prob=stockfish_move_prob,
        )

    if strategy == "elusive":
        return get_elusive_move(
            stockfish=stockfish,
            board=board,
            stockfish_move_prob=stockfish_move_prob,
        )

    if strategy == "predator":
        return get_predator_move(
            stockfish=stockfish,
            board=board,
            stockfish_move_prob=stockfish_move_prob,
        )

    if strategy == "monochrome":
        return get_monochrome_move(
            stockfish=stockfish,
            board=board,
            stockfish_move_prob=stockfish_move_prob,
        )

    if strategy == "dichrome":
        return get_dichrome_move(
            stockfish=stockfish,
            board=board,
            stockfish_move_prob=stockfish_move_prob,
        )

    if strategy == "checkmate-express":
        return get_checkmate_express_move(
            _stockfish=stockfish,
            board=board,
            _stockfish_move_prob=stockfish_move_prob,
        )

    raise Exception("Unknown strategy")
