from math import inf

from chess import SQUARES, Board, Move, square_name

from app.util.schema import ChessMove, MoveOutcome


def get_pieces_under_attack(*, board: Board, player_color: bool) -> list[int]:
    return [
        square
        for square in SQUARES
        if board.is_attacked_by(color=not player_color, square=square)
        and (piece := board.piece_at(square=square)) is not None
        and piece.color == player_color
    ]


def get_hypothetical_pieces_under_attack(
    *,
    board: Board,
    move: Move,
    player_color: bool,
) -> list[int]:
    hypothetical_board = board.copy()
    hypothetical_board.push(move=move)

    return get_pieces_under_attack(board=hypothetical_board, player_color=player_color)


def get_captured_piece_value(*, board: Board, move: Move) -> int:
    captured_piece = board.piece_at(square=move.to_square)
    return captured_piece.piece_type if captured_piece else 0


def get_board_value(*, board: Board, player_color: bool) -> int:
    value = 0

    for square in SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            if piece.color == player_color:
                value += piece.piece_type
            else:
                value -= piece.piece_type

    return value


def calculate_move_outcome_value(
    *,
    board: Board,
    move: Move,
    current_player_color: bool,
    depth: int,
) -> float:
    hypothetical_board = board.copy()
    hypothetical_board.push(move=move)

    if depth == 0 or hypothetical_board.is_checkmate():
        return get_board_value(
            board=hypothetical_board, player_color=current_player_color
        )

    if hypothetical_board.turn == current_player_color:
        max_value = -inf
        for move in hypothetical_board.legal_moves:
            value = calculate_move_outcome_value(
                board=hypothetical_board,
                move=move,
                current_player_color=current_player_color,
                depth=depth - 1,
            )
            max_value = max(max_value, value)
        return max_value
    else:
        min_value = inf
        for move in hypothetical_board.legal_moves:
            value = calculate_move_outcome_value(
                board=hypothetical_board,
                move=move,
                current_player_color=current_player_color,
                depth=depth - 1,
            )
            min_value = min(min_value, value)
        return min_value


def is_move_safety_improved(
    *,
    board: Board,
    move: Move,
    pieces_under_attack: list[int],
    current_player_color: bool,
) -> bool:
    return len(
        get_hypothetical_pieces_under_attack(
            board=board,
            move=move,
            player_color=current_player_color,
        )
    ) < len(pieces_under_attack)


def get_best_fortify_move(
    *,
    potential_moves: list[tuple[MoveOutcome, float]],
) -> MoveOutcome:
    return max(potential_moves, key=lambda move: move[1])[0]


def is_valid_move(*, board: Board, move: Move, pieces_under_attack: list[int]) -> bool:
    current_player_color = board.turn
    return (
        is_move_safety_improved(
            board=board,
            move=move,
            pieces_under_attack=pieces_under_attack,
            current_player_color=current_player_color,
        )
        or get_captured_piece_value(board=board, move=move) > 0
    )


def get_move_outcome(
    *,
    board: Board,
    move: Move,
    depth: int,
) -> tuple[MoveOutcome, float]:
    current_player_color = board.turn
    move_outcome = MoveOutcome(
        chess_move=ChessMove(
            from_square=square_name(square=move.from_square),
            to_square=square_name(square=move.to_square),
            promotion=square_name(square=move.promotion) if move.promotion else None,
        ),
    )
    outcome_value = calculate_move_outcome_value(
        board=board,
        move=move,
        current_player_color=current_player_color,
        depth=depth,
    )
    return move_outcome, outcome_value


def get_potential_fortify_moves(
    *,
    board: Board,
    pieces_under_attack: list[int],
    depth: int,
) -> list[tuple[MoveOutcome, float]]:
    return [
        get_move_outcome(board=board, move=move, depth=depth)
        for move in board.legal_moves
        if is_valid_move(
            board=board, move=move, pieces_under_attack=pieces_under_attack
        )
    ]
