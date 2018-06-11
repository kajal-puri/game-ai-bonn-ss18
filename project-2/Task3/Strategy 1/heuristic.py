import numpy as np

"""
Returns a score (integer or +/- infinity) of the state S.
The higher the score, the more favorable for player X 
the lower the score, the more favorable for player O 

The score is based on the heuristic that simply counts for each player the number of all
possible winning lines of magnitude i (from 1 .. k),
and weighs them, giving more points the bigger the i.
"""
def eval_game_state(S, n, m, k):
    # The i.th entry of each of the following arrays will contain
    # the number of possible winning lines of magnitude i for this player.
    # (N.B.: The 0.th entry is unused.)
    # (N.B.: If the k.th entry is > 0, then this player has won.)
    numWinLinesPlus = np.zeros(k+1, dtype=int)
    numWinLinesMinus = np.zeros(k+1, dtype=int)

    # For visual explanation of the following indices,
    # refer to the 'winning lines' image.

    # Diagonal lines (top left to bottom right)
    for i in range(0, n-k+1):
        for j in range(0, m-k+1):
            line = S[range(i, i+k),range(j, j+k)]
            eval_line(line, numWinLinesPlus, numWinLinesMinus)

    # Diagonal lines (bottom left to top right)
    for i in range(k-1, n):
        for j in range(0, m-k+1):
            line = S[range(i-(k-1), i+1),range(j, j+k)]
            eval_line(line, numWinLinesPlus, numWinLinesMinus)

    # Horizontal lines
    for i in range(0, n):
        for j in range(0, m-k+1):
            line = S[i, j:j+k]
            eval_line(line, numWinLinesPlus, numWinLinesMinus)

    # Vertical lines
    for i in range(k-1, n):
        for j in range(0, m):
            line = S[(i-k+1):(i+1), j]
            eval_line(line, numWinLinesPlus, numWinLinesMinus)

    # Special cases: One of the players has k discs connected.
    if (numWinLinesPlus[k] > 0 and numWinLinesMinus[k] > 0):
        raise Exception("Game state has two winners.")
    if (numWinLinesPlus[k] > 0):
        return +np.inf
    if (numWinLinesMinus[k] > 0):
        return -np.inf

    score = 0
    for x in range(1, k):
        score += 10**(x-1) * (numWinLinesPlus[x] - numWinLinesMinus[x])
    return score

"""
See eval_game_state for an explanation.
"""
def eval_line(line, numWinLinesPlus, numWinLinesMinus):
    # How many discs are there in the current line?
    numDiscsPlus = line[line == 1].size
    numDiscsMinus = line[line == -1].size

    # If there are discs from both players,
    # it is not a possible winning line.
    if numDiscsPlus > 0 and numDiscsMinus > 0:
        return

    # Update the corresponding array
    if numDiscsPlus > 0:
        numWinLinesPlus[numDiscsPlus] += 1
    else:
        numWinLinesMinus[numDiscsMinus] += 1
