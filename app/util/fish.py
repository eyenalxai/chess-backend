import subprocess

from stockfish import Stockfish


def get_executable_path(*, executable: str) -> str:
    path = subprocess.check_output(["which", executable])
    print(path.decode().strip())
    return path.decode().strip()


fish = Stockfish(path=get_executable_path(executable="stockfish"))
fish.set_skill_level(20)


def get_stockfish() -> Stockfish:
    yield fish
