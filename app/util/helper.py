from chess import square_rank, square_file, Square, Move, Board

from app.util.schema import StrategyName, ChessMove, MoveOutcome


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


def is_kamikaze_move(*, board: Board, move: Move) -> bool:
    hypothetical_board = board.copy()
    hypothetical_board.push(move)
    return hypothetical_board.is_attacked_by(hypothetical_board.turn, move.to_square)


def is_black_square(square: Square) -> bool:
    file = square_file(square)
    rank = square_rank(square)
    return (file + rank) % 2 != 0
