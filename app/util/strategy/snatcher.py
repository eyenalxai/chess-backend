from chess import Board, Move


def filter_punisher_moves(board: Board) -> list[Move]:
    return [move for move in board.legal_moves if board.is_capture(move)]
