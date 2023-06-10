import os

from stockfish import Stockfish

from app.util.settings import api_settings

fish = Stockfish(
    path=os.path.join(os.path.dirname(__file__), "stockfish")
    if api_settings.is_local
    else "/usr/games/stockfish"
)
fish.set_skill_level(20)


def get_stockfish() -> Stockfish:
    return fish
