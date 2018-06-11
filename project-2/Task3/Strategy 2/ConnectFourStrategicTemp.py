
import numpy as np
import random
import matplotlib.pyplot as plt
from numpy import unravel_index

GAMES_COUNT = 10


HIGHT = 6
WIDTH = 7
WINNING_NUMBER = 4


def move_still_possible(S):
    return not (S[S==0].size == 0)

# Return all column indices of columns
# in which there exists a free entry.
def column_with_empty_entries(S):
    return np.where(np.any(S==0, axis=0))[0]

def move_at_random(S,gsX,gsO, p):
    randomColumnIdx = random.choice(column_with_empty_entries(S))

    # Find the lowest entry (in terms of the board) of the random column,
    # s.t. this entry is still free.
    rowIdx = np.argmax(np.where(S.T[randomColumnIdx]==0))

    # Insert the player's token into the board.
    S[rowIdx,randomColumnIdx] = p
    if p ==1:
        gsO[rowIdx,randomColumnIdx] = 0
    else:
        gsX[rowIdx,randomColumnIdx] = 0
    return (S, rowIdx, randomColumnIdx)
def inteligent_move(S,gsX,gsO, p):
    mO = unravel_index(gsO.argmax(), gsO.shape)
    if gsO[mO] ==4:
        S[mO] = p
        gsO[mO] = 0
        gsX[mO] = 0
        return (S, mO[0],mO[1])
        
    else:
     mX = unravel_index(gsX.argmax(), gsX.shape)
     if gsX[mX] == 0:
         if S[HIGHT-1,WIDTH//2] == 0:
             S[HIGHT-1,WIDTH//2] = p
             gsO[HIGHT-1,WIDTH//2] = 0
             gsX[HIGHT-1,WIDTH//2] = 0
             return (S,HIGHT-1,WIDTH//2)
         else:
             S[HIGHT-1,(WIDTH//2)+1] = p
             gsO[HIGHT-1,(WIDTH//2)+1] = 0
             gsX[HIGHT-1,(WIDTH//2)+1] = 0
             return (S,HIGHT-1,(WIDTH//2)+1)
     else:
       S[mX] = p
       gsO[mX] = 0
       gsX[mX] = 0
       return (S,mX[0],mX[1])

# Returns true iff. the last move by player 'p' at ('lastMoveRow','lastMoveCol') was a winning move.
def move_was_winning_move(S, p, lastMoveRow, lastMoveCol):
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

def Score_updater(S, p, lastMoveRow, lastMoveCol):
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

    sumV = diskCounter
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

    sumH = diskCounter
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

    sumDbltr = diskCounter
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
    sumDtlbr = diskCounter
    ###########################################
    if sumV<4:
        if lastMoveRow+1 >= WIDTH or lastMoveRow-1 <=0:
            sumV =0
    if sumH<4:
        if lastMoveCol+1 >= HIGHT or lastMoveCol-1 <=0:
            sumH =0
    if sumDtlbr <4:
        if lastMoveRow+1 >= WIDTH or lastMoveCol+1 >= HIGHT or lastMoveRow-1 <= 0 or lastMoveCol-1 <= 0:
            sumDtlbr = 0
    if sumDbltr <4:
        if lastMoveRow+1 >= WIDTH or lastMoveCol+1 >= HIGHT or lastMoveRow-1 <= 0 or lastMoveCol-1 <= 0:
            sumDbltr = 0
    

    return max ([sumV,sumH,sumDbltr,sumDtlbr])








# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B
def updateScores(S,gsX,gsO,p):
    for i in range(HIGHT):
            for j in range(WIDTH):
                if S[i][j] == 0:
                    if i == HIGHT -1 or S[i+1][j] == p:
                      gsX[i][j] = Score_updater(S,1,i,j)
                      gsO[i][j] = Score_updater(S,-1,i,j)
        
def playGame ():
    gameState = np.zeros((HIGHT,WIDTH), dtype=int)
    gameScoresX = np.zeros((HIGHT,WIDTH), dtype=int)
    gameScoresO = np.zeros((HIGHT,WIDTH), dtype=int)

    # initialize player number, move counter
    player = -1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True
    

    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        print '%s moves' % name

        # let player move at random
        if player == -1:
            gameState, lastMoveRow, lastMoveCol = move_at_random(gameState,gameScoresX,gameScoresO, player)
        else:
            gameState, lastMoveRow, lastMoveCol = inteligent_move(gameState,gameScoresX,gameScoresO, player)
            

        # print current game state
        print_game_state(gameState)
        
        updateScores(gameState,gameScoresX,gameScoresO,player)
        
        
        
        # evaluate game state
        if move_was_winning_move(gameState, player, lastMoveRow, lastMoveCol):
            noWinnerYet = False
            print 'player %s wins after %d moves' % (name, mvcntr)
            print gameScoresX
            print gameScoresO

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1



    if noWinnerYet:
        print 'game ended in a draw' 

    return noWinnerYet, player * -1


if __name__ == '__main__':
    # initialize 6x7 connect four board
  counter = {-1: 0, 0: 0, 1: 0}
  for i in range(GAMES_COUNT):
    draw, winner = playGame()
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
  plt.title('Heuristic strategy for tic-tac-toe')
  plt.grid(True, axis='y')
  plt.show()

    