import os

from stockfish import Stockfish

fish = Stockfish(
    path=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "stockfish",
    )
)
fish.set_skill_level(20)


def get_stockfish() -> Stockfish:
    yield fish
