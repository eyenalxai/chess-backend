import os

from stockfish import Stockfish

from app.util.settings import api_settings


def get_stockfish_path() -> str:
    return (
        os.path.join(os.path.dirname(__file__), "stockfish")
        if api_settings.is_local
        else "/usr/games/stockfish"
    )


stockfish = Stockfish(path=get_stockfish_path())
stockfish.set_skill_level(20)
