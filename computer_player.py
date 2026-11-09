import random
import chess


PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 335,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}


def evaluate_position(board):
    """Score a position from White's point of view."""
    if board.is_checkmate():
        # The side whose turn it is has been checkmated.
        return -100_000 if board.turn == chess.WHITE else 100_000

    if board.is_game_over():
        return 0

    score = 0

    for square, piece in board.piece_map().items():
        value = PIECE_VALUES[piece.piece_type]

        # Small bonus for pieces near the center of the board.
        file_distance = abs(chess.square_file(square) - 3.5)
        rank_distance = abs(chess.square_rank(square) - 3.5)
        center_bonus = int(14 - 2 * (file_distance + rank_distance))

        piece_score = value + center_bonus
        score += piece_score if piece.color == chess.WHITE else -piece_score

    return score


def minimax(board, depth, alpha, beta):
    """Look ahead a few moves and return a position score."""
    if depth == 0 or board.is_game_over():
        return evaluate_position(board)

    legal_moves = list(board.legal_moves)

    # Look at captures first so the search can prune more quickly.
    legal_moves.sort(
        key=lambda move: board.is_capture(move),
        reverse=True,
    )

    if board.turn == chess.WHITE:
        best_score = float("-inf")

        for move in legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta)
            board.pop()

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return best_score

    best_score = float("inf")

    for move in legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, alpha, beta)
        board.pop()

        best_score = min(best_score, score)
        beta = min(beta, best_score)

        if beta <= alpha:
            break

    return best_score


def choose_move(board, difficulty="easy"):
    """Choose a legal move for the computer, which plays Black."""
    legal_moves = list(board.legal_moves)

    if not legal_moves:
        return None

    if board.turn != chess.BLACK:
        return None

    if difficulty == "easy":
        return random.choice(legal_moves)

    # Medium searches one reply ahead; hard searches further.
    search_depth = 1 if difficulty == "medium" else 2

    best_move = None
    best_score = float("inf")
    equally_good_moves = []

    for move in legal_moves:
        board.push(move)
        score = minimax(
            board,
            search_depth,
            float("-inf"),
            float("inf"),
        )
        board.pop()

        if score < best_score:
            best_score = score
            best_move = move
            equally_good_moves = [move]
        elif score == best_score:
            equally_good_moves.append(move)

    if equally_good_moves:
        return random.choice(equally_good_moves)

    return best_move