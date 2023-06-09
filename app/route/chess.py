from fastapi import APIRouter, Depends
from stockfish import Stockfish

from app.util.fish import get_stockfish
from app.util.move import execute_strategy, execute_move
from app.util.schema import MoveOutcome, StrategyRequest, ChessMove

chess_router = APIRouter(tags=["chess"])


@chess_router.post("/compute_move", response_model=MoveOutcome)
async def compute_move(
    strategy_request: StrategyRequest,
    stockfish: Stockfish = Depends(get_stockfish),
) -> MoveOutcome:
    return execute_strategy(
        strategy_request=strategy_request,
        stockfish=stockfish,
    )


@chess_router.post("/process_move", response_model=MoveOutcome)
async def process_move(
    chess_move: ChessMove,
    strategy_request: StrategyRequest,
) -> MoveOutcome:
    return execute_move(
        chess_move=chess_move,
        strategy_request=strategy_request,
    )
