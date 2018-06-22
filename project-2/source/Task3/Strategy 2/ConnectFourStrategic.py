
import numpy as np
import matplotlib.pyplot as plt
import random



HIGHT = 6
WIDTH = 7
WINNING_NUMBER = 4
GAMES_COUNT = 1


def move_still_possible(S):
    return not (S[S==0].size == 0)

# Return all column indices of columns
# in which there exists a free entry.
def column_with_empty_entries(S):
    return np.where(np.any(S==0, axis=0))[0]

def move_at_random(S, p):
    randomColumnIdx = random.choice(column_with_empty_entries(S))

    # Find the lowest entry (in terms of the board) of the random column,
    # s.t. this entry is still free.
    rowIdx = np.argmax(np.where(S.T[randomColumnIdx]==0))

    # Insert the player's token into the board.
    S[rowIdx,randomColumnIdx] = p
    return (S, rowIdx, randomColumnIdx)

# Returns true iff. the last move by player 'p' at ('lastMoveRow','lastMoveCol') was a winning move.
def move_was_winning_move(S,cellScores, p, lastMoveRow, lastMoveCol):
    # Each of the following cases counts the number of contiguous disks
    # player 'p' has set, starting from position ('lastMoveRow', 'lastMoveCol').
    # If there are at least WINNING_NUMBER many contiguous disks, player p has won.

    # Vertical check
    diskCounter = 1
    for i in range(1, WINNING_NUMBER):
        if lastMoveRow+i < HIGHT and S[lastMoveRow+i,lastMoveCol] == p:
            diskCounter += 1
            cellScores[lastMoveRow+i][lastMoveCol].score += 1
            print "cell ",lastMoveRow+i,",",lastMoveCol,"=",cellScores[lastMoveRow+i][lastMoveCol].score
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveRow-i >= 0 and S[lastMoveRow-i,lastMoveCol] == p:
            diskCounter += 1
            cellScores[lastMoveRow-i][lastMoveCol].score += 1
            print "cell ",lastMoveRow-i,",",lastMoveCol,"=",cellScores[lastMoveRow-i][lastMoveCol].score
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
            cellScores[lastMoveRow][lastMoveCol+i].score += 1
            print "cell ",lastMoveRow,",",lastMoveCol+i,"=",cellScores[lastMoveRow][lastMoveCol+i].score
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveCol-i >= 0 and S[lastMoveRow,lastMoveCol-i] == p:
            diskCounter += 1
            cellScores[lastMoveRow][lastMoveCol-i].score += 1
            print "cell ",lastMoveRow,",",lastMoveCol-i,"=",cellScores[lastMoveRow][lastMoveCol-i].score
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
            cellScores[lastMoveRow+i][lastMoveCol-i].score += 1
            print "cell ",lastMoveRow+i,",",lastMoveCol-i,"=",cellScores[lastMoveRow+i][lastMoveCol-i].score
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveRow-i >= 0 and lastMoveCol+i < WIDTH and S[lastMoveRow-i,lastMoveCol+i] == p:
            diskCounter += 1
            cellScores[lastMoveRow-i][lastMoveCol+i].score += 1
            print "cell ",lastMoveRow-i,",",lastMoveCol+i,"=",cellScores[lastMoveRow-i][lastMoveCol+i].score
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
            cellScores[lastMoveRow+i][lastMoveCol+i].score += 1
            print "cell ",lastMoveRow+i,",",lastMoveCol+i,"=",cellScores[lastMoveRow+i][lastMoveCol+i]
        else:
            break

    for i in range(1, WINNING_NUMBER):
        if lastMoveRow-i >= 0 and lastMoveCol-i >= 0 and S[lastMoveRow-i,lastMoveCol-i] == p:
            diskCounter += 1
            cellScores[lastMoveRow-i][lastMoveCol-i].score += 1
            print "cell ",lastMoveRow-i,",",lastMoveCol-i,"=",cellScores[lastMoveRow-i][lastMoveCol-i].score
        else:
            break

    if diskCounter >= WINNING_NUMBER:
        return True
    ###########################################

    return False

class boardCell(object):
    score = 0
    checked = False
    player = 0

def makeCell(score, checked, player):
    cell = boardCell()
    cell.score = score
    cell.checked = checked
    cell.player = player
    return cell




# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print (B)




def play_game():
    # initialize 6x7 connect four board
    gameState = np.zeros((HIGHT,WIDTH), dtype=int)
    
    cellScores = []
    for i in range(0, HIGHT):
        cellScore = []
        for j in range(0, WIDTH):
           a = makeCell(0,False,0)
           cellScore.append( a )    
           cellScores.append(cellScore)
            
 
    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True
    

    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        print ('%s moves' % name)

        # let player move at random
        gameState, lastMoveRow, lastMoveCol = move_at_random(gameState, player)

        # print current game state
        print_game_state(gameState)
        
        # evaluate game state
        if move_was_winning_move(gameState,cellScores, player, lastMoveRow, lastMoveCol):
            print ('player %s wins after %d moves' % (name, mvcntr))
            noWinnerYet = False

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1


    
    if noWinnerYet:
        print ('game ended in a draw') 
    return noWinnerYet, player * -1



if __name__ == '__main__':
    counter = {-1: 0, 0: 0, 1: 0}
    for i in range(GAMES_COUNT):
        draw, winner = play_game()
        if draw:
            counter[0] += 1
        else:
            counter[winner] += 1
    print counter

    ## Results Plot
    x = np.arange(3)
    x_heights = [counter[-1], counter[0], counter[1]]
    x_labels = ('Player O wins', 'Draw', 'Player X wins')
    plt.bar(x, x_heights)
    plt.xticks(x, x_labels)
    plt.ylabel('Number of games')
    plt.title('Random move in Connect Four')
    plt.grid(True, axis='y')
    plt.show()
