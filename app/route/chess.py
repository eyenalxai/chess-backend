from fastapi import APIRouter, Depends
from stockfish import Stockfish

from app.config.pydantic import Immutable
from app.util.fish import get_stockfish

chess_router = APIRouter(tags=["chess"])


class MoveRequest(Immutable):
    fen_string: str
    time: int


class ChessMove(Immutable):
    from_square: str
    to_square: str
    promotion: str | None = None


@chess_router.post("/stockfish", response_model=ChessMove)
async def get_best_move(
    move_request: MoveRequest,
    stockfish: Stockfish = Depends(get_stockfish),
) -> ChessMove:
    if not stockfish.is_fen_valid(move_request.fen_string):
        raise Exception("FEN is not valid")

    stockfish.set_fen_position(move_request.fen_string)
    best_move = stockfish.get_best_move_time(move_request.time or 1000)

    if not best_move:
        raise Exception("No best move found")

    if len(best_move) == 4:
        return ChessMove(
            from_square=best_move[:2],
            to_square=best_move[2:],
        )

    if len(best_move) == 5:
        return ChessMove(
            from_square=best_move[:2],
            to_square=best_move[2:4],
            promotion=best_move[4],
        )

    raise Exception("Invalid best move")
