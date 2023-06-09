from chess import (
    Board,
    Termination,
    Outcome,
    Move,
    square_name,
)
from stockfish import Stockfish

from app.util.schema import (
    MoveOutcome,
    StrategyRequest,
    GameOutcome,
    Winner,
    Reason,
    ChessMove,
)
from app.util.strategy import (
    get_pawnstorm_move,
    get_predator_move,
    get_kamikaze_move,
    get_same_color_move,
    get_stockfish_move,
    get_random_move,
    get_pacifist_move,
    get_opposite_color_move,
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

    if strategy_request.strategy_name.startswith("stockfish"):
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name=strategy_request.strategy_name,
            fen_string=strategy_request.fen_string,
        )

    if strategy_request.strategy_name == "random":
        return get_random_move(
            board=board,
        )

    if strategy_request.strategy_name == "pacifist":
        return get_pacifist_move(
            board=board,
        )

    if strategy_request.strategy_name == "pawnstorm":
        return get_pawnstorm_move(
            board=board,
        )

    if strategy_request.strategy_name == "predator":
        return get_predator_move(
            board=board,
        )

    if strategy_request.strategy_name == "kamikaze":
        return get_kamikaze_move(
            board=board,
        )

    if strategy_request.strategy_name == "same-color":
        return get_same_color_move(
            board=board,
        )

    if strategy_request.strategy_name == "opposite-color":
        return get_opposite_color_move(
            board=board,
        )

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
