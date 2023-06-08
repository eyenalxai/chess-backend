from stockfish import Stockfish


fish = Stockfish(path="/usr/games/stockfish")
fish.set_skill_level(20)


def get_stockfish() -> Stockfish:
    yield fish
