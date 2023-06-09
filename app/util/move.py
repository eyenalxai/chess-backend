from random import choice

from chess import Board, Termination, Outcome, Move, square_name
from stockfish import Stockfish

from app.util.schema import (
    MoveOutcome,
    StrategyRequest,
    StrategyName,
    GameOutcome,
    Winner,
    Reason,
    ChessMove,
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


def parse_move(*, move: str) -> MoveOutcome:
    if len(move) == 4:
        return MoveOutcome(
            chess_move=ChessMove(
                from_square=move[:2],
                to_square=move[2:],
            )
        )

    if len(move) == 5:
        return MoveOutcome(
            chess_move=ChessMove(
                from_square=move[:2],
                to_square=move[2:4],
                promotion=move[4],
            )
        )

    raise Exception("Invalid best move")


def get_time_for_strategy(strategy: StrategyName) -> int:
    if strategy == "stockfish-1":
        return 1
    if strategy == "stockfish-10":
        return 10
    if strategy == "stockfish-100":
        return 100
    if strategy == "stockfish-500":
        return 500
    if strategy == "stockfish-1000":
        return 1000

    raise Exception("Invalid strategy")


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


def get_pacifist_move(*, board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())
    pacifist_moves = [move for move in legal_moves if not board.is_capture(move)]

    if not pacifist_moves:
        return get_random_move(board=board)

    return parse_move(move=choice(pacifist_moves).uci())


def get_predator_move(*, board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())
    pacifist_moves = [move for move in legal_moves if board.is_capture(move)]

    if not pacifist_moves:
        return get_random_move(board=board)

    return parse_move(move=choice(pacifist_moves).uci())


def get_pawnstorm_move(*, board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())
    pieces = board.piece_map()

    # Gets a list of all the pawn squares on the board.
    pawn_squares = [
        square for square, piece in pieces.items() if piece.symbol().lower() == "p"
    ]

    pawn_moves = [move for move in legal_moves if move.from_square in pawn_squares]

    if not pawn_moves:
        return get_random_move(board=board)

    capture_moves = [move for move in pawn_moves if board.is_capture(move)]
    non_capture_moves = [move for move in pawn_moves if not board.is_capture(move)]

    if capture_moves:
        return parse_move(move=choice(capture_moves).uci())

    return parse_move(move=choice(non_capture_moves).uci())


def get_winner(*, outcome: Outcome) -> Winner:
    if outcome.winner is None:
        return "draw"

    if outcome.winner:
        return "white"

    return "black"


def is_kamikaze_move(*, board: Board, move: Move) -> bool:
    hypothetical_board = board.copy()
    hypothetical_board.push(move)
    return hypothetical_board.is_attacked_by(hypothetical_board.turn, move.to_square)


def get_kamikaze_move(*, board: Board) -> MoveOutcome:
    legal_moves = list(board.generate_legal_moves())

    kamikaze_moves = [
        move for move in legal_moves if is_kamikaze_move(board=board, move=move)
    ]

    if kamikaze_moves:
        return parse_move(move=choice(kamikaze_moves).uci())

    print("No kamikaze moves found")

    return get_pacifist_move(board=board)


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
