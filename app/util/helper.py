from chess import (
    PIECE_NAMES,
    PIECE_SYMBOLS,
    Board,
    Move,
    Outcome,
    Piece,
    Square,
    Termination,
    square_file,
    square_rank,
)

from app.util.schema import (
    ChessMove,
    GameOutcome,
    MoveOutcome,
    Reason,
    StrategyName,
    Winner,
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

PIECE_VALUES = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 100}


def get_game_outcome(*, board: Board) -> MoveOutcome | None:
    if board.is_game_over():
        outcome = board.outcome()
        if outcome is not None:
            winner = get_winner(outcome=outcome)
            reason = TERMINATION_REASON.get(outcome.termination)
            if reason is not None:
                return MoveOutcome(
                    game_outcome=GameOutcome(
                        winner=winner,
                        reason=reason,
                        ended=True,
                    )
                )
            raise Exception("Invalid reason")
        raise Exception("Invalid outcome")

    return None


def get_winner(*, outcome: Outcome) -> Winner:
    if outcome.winner is None:
        return "draw"

    if outcome.winner:
        return "white"

    return "black"


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


def get_time_for_stockfish_strategy(strategy: StrategyName) -> int:
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


def is_kamikaze_move(*, board: Board, move: Move) -> bool:
    if not board.is_capture(move=move):
        return False

    hypothetical_board = board.copy()
    hypothetical_board.push(move=move)

    if hypothetical_board.is_attacked_by(
        color=not hypothetical_board.turn,
        square=move.to_square,
    ):
        return True

    return False


def is_black_square(square: Square) -> bool:
    file = square_file(square=square)
    rank = square_rank(square=square)
    return (file + rank) % 2 != 0


def get_piece_value(*, piece: Piece | None) -> int:
    return PIECE_VALUES.get(piece.symbol().upper(), 0) if piece else 0


def get_best_capture(
    *,
    legal_moves: list[Move],
    board: Board,
) -> tuple[Move, int] | None:
    captures: list[tuple[Move, int]] = [
        (move, get_piece_value(piece=board.piece_at(move.to_square)))
        for move in legal_moves
        if board.is_capture(move)
    ]
    try:
        return max(captures, key=lambda x: x[1])
    except ValueError:
        return None


def get_piece_type(name: str | None) -> int | None:
    if name is None:
        return None
    if name in PIECE_SYMBOLS:
        return PIECE_SYMBOLS.index(name)
    if name in PIECE_NAMES:
        return PIECE_NAMES.index(name)
    return None
