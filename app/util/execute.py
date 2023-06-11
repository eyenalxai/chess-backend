from typing import Callable

from chess import Board, Move, square_name
from stockfish import Stockfish

from app.util.board_evaluation import count_opponent_pieces
from app.util.game_outcome import get_game_outcome
from app.util.move import (
    get_chroma_move,
    get_contrast_move,
    get_dodger_move,
    get_punisher_move,
    get_random_move,
    get_stockfish_move,
)
from app.util.schema import ChessMove, MoveOutcome, StrategyName, StrategyRequest

STRATEGY_FUNCTIONS: dict[
    StrategyName, tuple[Callable[[Stockfish, Board, float], MoveOutcome], float]
] = {
    "random": (get_random_move, 0),
    "dodger": (get_dodger_move, 1 / 10),
    "punisher": (get_punisher_move, 1 / 10),
    "chroma": (get_chroma_move, 1 / 5),
    "contrast": (get_contrast_move, 1 / 5),
}


def execute_strategy(
    *,
    strategy_request: StrategyRequest,
    stockfish: Stockfish,
) -> MoveOutcome:
    board = Board(fen=strategy_request.fen_string)

    if (
        not strategy_request.strategy_name.startswith("stockfish")
        and count_opponent_pieces(board=board, player_color=board.turn) == 1
    ):
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name="stockfish-10",
            fen_string=strategy_request.fen_string,
        )

    game_outcome = get_game_outcome(board=board)

    if game_outcome is not None:
        return game_outcome

    if strategy_request.strategy_name.startswith("stockfish"):
        return get_stockfish_move(
            stockfish=stockfish,
            strategy_name=strategy_request.strategy_name,
            fen_string=strategy_request.fen_string,
        )

    strategy_function, probability = STRATEGY_FUNCTIONS.get(
        strategy_request.strategy_name, (None, 0)
    )

    if strategy_function:
        return strategy_function(stockfish, board, probability)

    raise Exception("Invalid strategy")


def execute_move(
    *,
    chess_move: ChessMove,
    strategy_request: StrategyRequest,
) -> MoveOutcome:
    board = Board(fen=strategy_request.fen_string)

    uci_string = "".join([chess_move.from_square, chess_move.to_square])
    if chess_move.promotion:
        uci_string = "".join([uci_string, chess_move.promotion])

    move = Move.from_uci(uci=uci_string)

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
            uci=move.uci(),
        ),
        game_outcome=None,
    )
