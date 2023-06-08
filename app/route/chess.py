from fastapi import APIRouter, Depends
from stockfish import Stockfish

from app.util.fish import get_stockfish
from app.util.move import get_move
from app.util.schema import ChessMove, MoveRequest

chess_router = APIRouter(tags=["chess"])


@chess_router.post("/chess", response_model=ChessMove)
async def get_best_move(
    move_request: MoveRequest,
    stockfish: Stockfish = Depends(get_stockfish),
) -> ChessMove:
    return get_move(
        move_request=move_request,
        stockfish=stockfish,
    )
