from chess import Move, Board

from app.util.board_evaluation import (
    simulate_move_and_evaluate,
    NoMovesToEvaluateError,
    evaluate_and_get_optimal_move,
)
from app.util.schema import MoveEvaluation


def get_worst_move_based_on_opponent_response(
    *,
    board: Board,
    player_move: Move,
) -> MoveEvaluation | None:
    hypothetical_board = board.copy(stack=False)
    hypothetical_board.push(player_move)
    opponent_moves = list(hypothetical_board.legal_moves)

    try:
        best_opponent_move = evaluate_and_get_optimal_move(
            board=hypothetical_board,
            moves=opponent_moves,
            is_max=True,
        )
    except NoMovesToEvaluateError:
        return None

    return MoveEvaluation(
        move=player_move,
        value=simulate_move_and_evaluate(
            board=hypothetical_board,
            move=best_opponent_move,
        ),
    )


def get_worst_moves(*, board: Board, player_moves: list[Move]) -> list[MoveEvaluation]:
    worst_moves = []
    for player_move in player_moves:
        move_evaluation = get_worst_move_based_on_opponent_response(
            board=board,
            player_move=player_move,
        )
        if move_evaluation is not None:
            worst_moves.append(move_evaluation)
    return worst_moves
