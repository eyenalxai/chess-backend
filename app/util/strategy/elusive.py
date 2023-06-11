from chess import Board, Move

from app.util.board_evaluation import get_pieces_under_attack


def filter_elusive_moves(board: Board) -> list[Move]:
    pieces_under_attack = get_pieces_under_attack(
        board=board,
        player_color=board.turn,
    )

    return [
        move for move in board.legal_moves if move.from_square in pieces_under_attack
    ]
