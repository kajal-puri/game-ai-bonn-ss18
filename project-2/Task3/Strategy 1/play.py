from alphabeta import *

def play_game(depth):
    # initialize n*m connect four board
    gameState = np.zeros((HIGHT,WIDTH), dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True

    while move_still_possible(gameState) and noWinnerYet:
        # Human player
        if player == -1:
            col = input("Column: ")
            best_move = do_move(gameState, player, col)
        # Alphabeta player
        elif player == 1:
            best_move = alphabeta(gameState, depth, -np.inf, +np.inf, player)
            gameState[best_move[0], best_move[1]] = player

        # print current game state
        print mvcntr, "   turn", player
        print_game_state(gameState)
        print "   0,  1,  2,  3,  4,  5,  6"

        # evaluate game state
        if move_was_winning_move(gameState, *best_move):
            print 'player %s wins after %d moves' % (player, mvcntr)
            noWinnerYet = False

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1



    if noWinnerYet:
        print 'game ended in a draw'

if __name__ == '__main__':
    play_game(depth=4)
