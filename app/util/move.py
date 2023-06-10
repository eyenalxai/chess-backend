from typing import Callable

from chess import Board, Move, Outcome, Termination, square_name
from stockfish import Stockfish  # type: ignore

from app.util.schema import (
    ChessMove,
    GameOutcome,
    MoveOutcome,
    Reason,
    StrategyName,
    StrategyRequest,
    Winner,
)
from app.util.strategy import (
    get_chroma_move,
    get_contrast_move,
    get_kamikaze_move,
    get_pacifist_move,
    get_pawnstorm_move,
    get_predator_move,
    get_random_move,
    get_stockfish_move,
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


def get_winner(*, outcome: Outcome) -> Winner:
    if outcome.winner is None:
        return "draw"

    if outcome.winner:
        return "white"

    return "black"


def get_game_outcome(*, board: Board) -> MoveOutcome | None:
    if board.is_game_over():
        outcome = board.outcome()
        if outcome is not None:
            winner = get_winner(outcome=outcome)
            reason = TERMINATION_REASON.get(outcome.termination)
            if reason is not None:
                return MoveOutcome(
                    game_outcome=GameOutcome(winner=winner, reason=reason, ended=True)
                )
            raise Exception("Invalid reason")
        raise Exception("Invalid outcome")

    return None


def execute_strategy(
    *,
    strategy_request: StrategyRequest,
    stockfish: Stockfish,
) -> MoveOutcome:
    board = Board(fen=strategy_request.fen_string)

    game_outcome = get_game_outcome(board=board)

    if game_outcome is not None:
        return game_outcome

    strategy_functions: dict[StrategyName, Callable[[Board], MoveOutcome]] = {
        "random": get_random_move,
        "pacifist": get_pacifist_move,
        "pawnstorm": get_pawnstorm_move,
        "predator": get_predator_move,
        "kamikaze": get_kamikaze_move,
        "chroma": get_chroma_move,
        "contrast": get_contrast_move,
    }

    if strategy_request.strategy_name.startswith("stockfish"):
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name=strategy_request.strategy_name,
            fen_string=strategy_request.fen_string,
        )

    strategy_function = strategy_functions.get(strategy_request.strategy_name)

    if strategy_function:
        return strategy_function(board)

    raise Exception("Invalid strategy")


def execute_move(
    *,
    chess_move: ChessMove,
    strategy_request: StrategyRequest,
) -> MoveOutcome:
    board = Board(fen=strategy_request.fen_string)

    uci_string = chess_move.from_square + chess_move.to_square
    if chess_move.promotion:
        uci_string += chess_move.promotion

    move = Move.from_uci(uci_string)

    legal_move_ucis = [legal_move.uci() for legal_move in board.legal_moves]

    if move.uci() not in legal_move_ucis and move.uci()[0:4] not in legal_move_ucis:
        raise Exception("Invalid move")

    board.push(move)

    game_outcome = get_game_outcome(board=board)

    if game_outcome is not None:
        return game_outcome

    return MoveOutcome(
        chess_move=ChessMove(
            from_square=square_name(square=move.from_square),
            to_square=square_name(square=move.to_square),
            promotion=chess_move.promotion,
        ),
        game_outcome=None,
    )
