from collections.abc import Callable
from random import choice

from chess import Board, Move
from stockfish import Stockfish

from app.util.helper import (
    evaluate_and_get_best_move,
    get_time_for_stockfish_strategy,
    parse_move,
    should_do_stockfish_move,
)
from app.util.schema import MoveOutcome, StrategyName
from app.util.strategy.chroma import filter_chroma_moves
from app.util.strategy.contrast import filter_contrast_moves
from app.util.strategy.dodger import filter_dodger_moves
from app.util.strategy.punisher import filter_punisher_moves


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
        move_uci=evaluate_and_get_best_move(
            board=board,
            moves=filtered_moves,
            player_color=board.turn,
        ).uci()
    )


def get_dodger_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float = 0.1,
) -> MoveOutcome:
    return get_move(
        stockfish=stockfish,
        board=board,
        stockfish_move_prob=stockfish_move_prob,
        filter_moves=filter_dodger_moves,
    )


def get_punisher_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
) -> MoveOutcome:
    return get_move(
        stockfish=stockfish,
        board=board,
        stockfish_move_prob=stockfish_move_prob,
        filter_moves=filter_punisher_moves,
    )


def get_chroma_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
) -> MoveOutcome:
    return get_move(
        stockfish=stockfish,
        board=board,
        stockfish_move_prob=stockfish_move_prob,
        filter_moves=filter_chroma_moves,
    )


def get_contrast_move(
    stockfish: Stockfish,
    board: Board,
    stockfish_move_prob: float,
) -> MoveOutcome:
    return get_move(
        stockfish=stockfish,
        board=board,
        stockfish_move_prob=stockfish_move_prob,
        filter_moves=filter_contrast_moves,
    )
