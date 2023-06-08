from random import choice

from chess import Board, Termination, Outcome
from stockfish import Stockfish

from app.util.schema import (
    ChessMove,
    MoveRequest,
    StrategyName,
    GameOutcome,
    Winner,
    Reason,
)

TERMINATION_REASON: dict[Termination, Reason] = {
    Termination.CHECKMATE: "checkmate",
    Termination.STALEMATE: "stalemate",
    Termination.INSUFFICIENT_MATERIAL: "insufficient_material",
    Termination.SEVENTYFIVE_MOVES: "seventyfive_moves",
    Termination.FIVEFOLD_REPETITION: "fivefold_repetition",
    Termination.FIFTY_MOVES: "fifty_moves",
    Termination.THREEFOLD_REPETITION: "threefold_repetition",
    Termination.VARIANT_WIN: "variant_win",
    Termination.VARIANT_LOSS: "variant_loss",
    Termination.VARIANT_DRAW: "variant_draw",
}


def parse_move(*, move: str) -> ChessMove:
    if len(move) == 4:
        return ChessMove(
            from_square=move[:2],
            to_square=move[2:],
        )

    if len(move) == 5:
        return ChessMove(
            from_square=move[:2],
            to_square=move[2:4],
            promotion=move[4],
        )

    raise Exception("Invalid best move")


def get_time_for_strategy(strategy: StrategyName) -> int:
    if strategy == "stockfish-100":
        return 100
    if strategy == "stockfish-500":
        return 500
    if strategy == "stockfish-1000":
        return 1000
    return 0


def get_stockfish_move(
    *,
    stockfish: Stockfish,
    strategy_name: StrategyName,
    fen_string: str,
) -> ChessMove:
    stockfish.set_fen_position(fen_position=fen_string)
    time = get_time_for_strategy(strategy=strategy_name)
    best_move = stockfish.get_best_move_time(time=time)

    if not best_move:
        raise Exception("No best move found")

    return parse_move(move=best_move)


def get_random_move(
    *,
    board: Board,
) -> ChessMove:
    return parse_move(move=choice(list(board.generate_legal_moves())).uci())


def get_pacifist_move(*, board: Board) -> ChessMove:
    legal_moves = list(board.generate_legal_moves())
    pacifist_moves = [move for move in legal_moves if not board.is_capture(move)]

    if not pacifist_moves:
        return get_random_move(board=board)

    return parse_move(move=choice(pacifist_moves).uci())


def get_winner(*, outcome: Outcome) -> Winner:
    if outcome.winner is None:
        return "draw"

    if outcome.winner:
        return "white"

    return "black"


def get_move(*, move_request: MoveRequest, stockfish: Stockfish) -> ChessMove:
    board = Board(fen=move_request.fen_string)

    if board.legal_moves.count() == 0:
        outcome = board.outcome()
        if outcome is not None:
            winner = get_winner(outcome=outcome)
            reason = TERMINATION_REASON.get(outcome.termination)
            if reason is not None:
                return ChessMove(
                    game_outcome=GameOutcome(winner=winner, reason=reason, ended=True)
                )

            raise Exception("Invalid reason")

        raise Exception("Invalid outcome")

    if move_request.strategy_name.startswith("stockfish"):
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name=move_request.strategy_name,
            fen_string=move_request.fen_string,
        )

    if move_request.strategy_name == "random":
        return get_random_move(
            board=board,
        )

    if move_request.strategy_name == "pacifist":
        return get_pacifist_move(
            board=board,
        )

    raise Exception("Invalid strategy")
