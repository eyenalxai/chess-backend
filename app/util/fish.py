import os
import platform

from stockfish import Stockfish

print("OS:", os.name)
print("CWD:", os.getcwd())
print("UNAME:", os.uname())
print("PLATFORM", platform.machine())

fish = Stockfish(
    path=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "stockfish",
    )
)
fish.set_skill_level(20)


def get_stockfish() -> Stockfish:
    yield fish
