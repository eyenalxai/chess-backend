from chess import BLACK, WHITE, Board

from app.util.board_evaluation import (
    count_opponent_pieces,
    evaluate_and_get_optimal_move,
    evaluate_board,
)


def test_evaluate_board() -> None:
    board = Board(fen="k7/8/8/8/8/8/8/K7 w - - 0 1")

    assert evaluate_board(board=board, player_color=WHITE) == 0
    assert evaluate_board(board=board, player_color=BLACK) == 0

    board = Board(fen="k1q5/8/8/8/8/8/8/K7 w - - 0 1")

    assert evaluate_board(board=board, player_color=WHITE) == -9
    assert evaluate_board(board=board, player_color=BLACK) == 9

    board = Board(fen="k1qrbnpp/8/8/8/8/8/8/K1QRBNPP w - - 0 1")

    assert evaluate_board(board=board, player_color=WHITE) == 0
    assert evaluate_board(board=board, player_color=BLACK) == 0

    board = Board(fen="k1qrbnpp/8/8/8/8/8/5PP1/K1QRBNPP w - - 0 1")

    assert evaluate_board(board=board, player_color=WHITE) == 2
    assert evaluate_board(board=board, player_color=BLACK) == -2


def test_simulate_move_and_evaluate() -> None:
    board = Board(fen="k7/8/8/8/4p3/3Q1N2/8/K7 b - - 0 1")
    ending_fen = "k7/8/8/8/8/3p1N2/8/K7 w - - 0 2"

    best_move = evaluate_and_get_optimal_move(
        board=board,
        moves=list(board.legal_moves),
    )

    board.push(move=best_move)

    assert board.fen() == ending_fen

    board = Board(fen="K7/8/8/3n1n2/2r3q1/4N3/2b3r1/k2b1p2 w - - 0 1")
    ending_fen = "K7/8/8/3n1n2/2r3N1/8/2b3r1/k2b1p2 b - - 0 1"

    best_move = evaluate_and_get_optimal_move(
        board=board,
        moves=list(board.legal_moves),
    )

    board.push(move=best_move)

    assert board.fen() == ending_fen

    board = Board(fen="3k4/3n4/1p6/4Q3/2R5/6p1/7P/K7 b - - 0 1")
    ending_fen = "3k4/8/1p6/4n3/2R5/6p1/7P/K7 w - - 0 2"

    best_move = evaluate_and_get_optimal_move(
        board=board,
        moves=list(board.legal_moves),
    )

    board.push(move=best_move)

    assert board.fen() == ending_fen


def test_count_opponent_pieces() -> None:
    board = Board(fen="k1qrb2P/2p3p1/2P1P1P1/2P5/P2p4/4PPp1/8/K4P2 w - - 0 1")

    assert count_opponent_pieces(board=board, player_color=BLACK) == 10
    assert count_opponent_pieces(board=board, player_color=WHITE) == 8
