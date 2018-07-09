from alphabeta import *

def simulate_game(depth):
    # Count number of wins
    xWins = 0
    oWins = 0

    # initialize n*m connect four board
    gameState = np.zeros((HIGHT,WIDTH), dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True

    while move_still_possible(gameState) and noWinnerYet:
        # let player move at random
        if player == -1:
            best_move = move_at_random(gameState, player)
            gameState[best_move[0], best_move[1]] = player
        # Alphabeta player
        elif player == 1:
            best_move = alphabeta(gameState, depth, -np.inf, +np.inf, player)
            gameState[best_move[0], best_move[1]] = player

        # evaluate game state
        if move_was_winning_move(gameState, *best_move):
            if player == 1:
                xWins += 1
            elif player == -1:
                oWins += 1
            noWinnerYet = False

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1

    if noWinnerYet:
        print 'game ended in a draw'

    return (xWins, oWins)

if __name__ == '__main__':
    for depth in range(1, 5):
        plusTotalWins = 0
        minusTotalWins = 0
        for i in range(0, 1000):
            (xWins, oWins) = simulate_game(depth=depth)
            plusTotalWins += xWins
            minusTotalWins += oWins

        print 'depth: %d' % depth
        print 'player  1 (x) won %d times' % plusTotalWins
        print 'player -1 (o) won %d times' % minusTotalWins
