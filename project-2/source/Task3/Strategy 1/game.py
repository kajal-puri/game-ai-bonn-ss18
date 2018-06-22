import numpy as np
import random

HIGHT = 6
WIDTH = 7
WINNING_NUMBER = 4


def move_still_possible(S):
    return not (S[S == 0].size == 0)

"""
Return all column indices of columns
in which there exists a free entry.
"""
def column_with_empty_entries(S):
    return np.where(np.any(S.T == 0, axis=1))[0]

def do_move(S, p, col):
    # Find the lowest entry (in terms of the board) of the random column,
    # s.t. this entry is still free.
    rowIdx = np.argmax(np.where(S.T[col] == 0))

    # Insert the player's token into the board.
    S[rowIdx, col] = p
    return (rowIdx, col)


def undo_move(S, row, col):
    S[row, col] = 0


# Returns true iff. the last move at ('lastMoveRow','lastMoveCol') was a winning move.
def move_was_winning_move(S, lastMoveRow, lastMoveCol):
    p = S[lastMoveRow, lastMoveCol]
    if p == 0:
        raise Exception("move_was_winning_move(): Last move invalid.")

    # Each of the following cases counts the number of contiguous disks
    # player 'p' has set, starting from position ('lastMoveRow', 'lastMoveCol').
    # If there are at least WINNING_NUMBER many contiguous disks, player p has won.

    # Vertical check
    diskCounter = 1
    for i in range(1, WINNING_NUMBER):
        if lastMoveRow+i < HIGHT and S[lastMoveRow+i,lastMoveCol] == p:
            diskCounter += 1
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveRow-i >= 0 and S[lastMoveRow-i,lastMoveCol] == p:
            diskCounter += 1
        else:
            break

    if diskCounter >= WINNING_NUMBER:
        return True
    ###########################################

    # Horizontal check
    diskCounter = 1
    for i in range(1, WINNING_NUMBER):
        if lastMoveCol+i < WIDTH and S[lastMoveRow,lastMoveCol+i] == p:
            diskCounter += 1
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveCol-i >= 0 and S[lastMoveRow,lastMoveCol-i] == p:
            diskCounter += 1
        else:
            break

    if diskCounter >= WINNING_NUMBER:
        return True
    ###########################################

    # Diagonal check (bottom left to top right)
    diskCounter = 1
    for i in range(1, WINNING_NUMBER):
        if lastMoveRow+i < HIGHT and lastMoveCol-i >= 0 and S[lastMoveRow+i,lastMoveCol-i] == p:
            diskCounter += 1
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveRow-i >= 0 and lastMoveCol+i < WIDTH and S[lastMoveRow-i,lastMoveCol+i] == p:
            diskCounter += 1
        else:
            break

    if diskCounter >= WINNING_NUMBER:
        return True
    ###########################################

    # Diagonal check (top left to bottom right)
    diskCounter = 1
    for i in range(1, WINNING_NUMBER):
        if lastMoveRow+i < HIGHT and lastMoveCol+i < WIDTH and S[lastMoveRow+i,lastMoveCol+i] == p:
            diskCounter += 1
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveRow-i >= 0 and lastMoveCol-i >= 0 and S[lastMoveRow-i,lastMoveCol-i] == p:
            diskCounter += 1
        else:
            break

    if diskCounter >= WINNING_NUMBER:
        return True
    ###########################################

    return False

def move_at_random(S, p):
    randomColumnIdx = random.choice(column_with_empty_entries(S))

    # Find the lowest entry (in terms of the board) of the random column,
    # s.t. this entry is still free.
    rowIdx = np.argmax(np.where(S.T[randomColumnIdx]==0))

    # Insert the player's token into the board.
    S[rowIdx,randomColumnIdx] = p
    return (rowIdx, randomColumnIdx)

# print game state matrix using symbols
def print_game_state(S):
    symbols = {1:'x', -1:'o', 0:'_'}
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B, '\n'
