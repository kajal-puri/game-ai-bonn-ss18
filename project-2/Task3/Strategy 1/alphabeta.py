from game import *
from heuristic import *

def alphabeta(S, depth, alpha, beta, player):
    return alphabeta_(S, depth, depth, alpha, beta, player, -1, -1)

def alphabeta_(S, original_depth, depth, alpha, beta, player, lastmove_row, lastmove_col):
    if original_depth <= 0:
        raise Exception("Search depth has to be > 0.")

    if original_depth != depth and move_was_winning_move(S, lastmove_row, lastmove_col):
        return -player * np.inf
    elif not move_still_possible(S):
        return 0
    elif depth == 0:
        return eval_game_state(S, HIGHT, WIDTH, WINNING_NUMBER)

    if original_depth == depth:
        children = column_with_empty_entries(S)
        for child in children:
            (row, col) = do_move(S, player, child)

            alpha_new = alphabeta_(S, original_depth, depth-1, alpha, beta, -player, row, col)
            if alpha < alpha_new:
                alpha = alpha_new
                best_move = (row, col)

            undo_move(S, row, col)
            if beta <= alpha:
                break  # beta cut-off
        try:
            return best_move
        except NameError:
            return do_move(S, player, random.choice(children))
    elif player == 1:
        children = column_with_empty_entries(S)
        for child in children:
            (row, col) = do_move(S, player, child)
            alpha = max(alpha, alphabeta_(S, original_depth, depth-1, alpha, beta, -player, row, col))
            undo_move(S, row, col)
            if beta <= alpha:
                break  # beta cut-off
        return alpha
    elif player == -1:
        children = column_with_empty_entries(S)
        for child in children:
            (row, col) = do_move(S, player, child)
            beta = min(beta, alphabeta_(S, original_depth, depth-1, alpha, beta, -player, row, col))
            undo_move(S, row, col)
            if beta <= alpha:
                break  # alpha cut-off
        return beta
