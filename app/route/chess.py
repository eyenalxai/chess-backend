from fastapi import APIRouter, Depends
from stockfish import Stockfish

from app.util.fish import get_stockfish
from app.util.move import execute_strategy
from app.util.schema import MoveOutcome, StrategyRequest

chess_router = APIRouter(tags=["chess"])


@chess_router.post("/chess", response_model=MoveOutcome)
async def compute_move(
    strategy_request: StrategyRequest,
    stockfish: Stockfish = Depends(get_stockfish),
) -> MoveOutcome:
    return execute_strategy(
        move_request=strategy_request,
        stockfish=stockfish,
    )
