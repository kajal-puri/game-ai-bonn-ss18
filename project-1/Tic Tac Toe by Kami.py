

import numpy as np
import matplotlib.pyplot as plt
import pickle
import collections
 
with open('prob.pickle', 'rb') as handle:
    prob = pickle.load(handle)

def move_still_possible(S):
    return not (S[S==0].size == 0)
    
    
def move_at_random(S, p):
    xs, ys = np.where(S==0)

    i = np.random.permutation(np.arange(xs.size))[0]
    
    S[xs[i],ys[i]] = p

    return S


def move(S, p):
    
    #xs, ys = np.where(S==0)
    copyGameState = np.copy(S).astype(object)
    copyProb = np.copy(prob).astype(object)
    copyProb[copyGameState != 0] = 0 
    maximumProb = copyProb.max()
    xs, ys = np.where(copyProb == maximumProb)
    
    S[xs[0],ys[0]] = p

    return S


def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False



# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    #print (B)


def simulate(times = 10):
    
    winner = []
    winnerEncoded = []    
    for i in range(times):
        # initialize 3x3 tic tac toe board
        gameState = np.zeros((3,3), dtype=int)
    
        # initialize player number, move counter
        player = 1
        mvcntr = 1
    
        # initialize flag that indicates win
        noWinnerYet = True
        
    
        while move_still_possible(gameState) and noWinnerYet:
            # get player symbol
            #name = symbols[player]
    
            # let player move at random
            if(player == 1):
                gameState = move(gameState, player)
                
            if(player == -1):
                gameState = move_at_random(gameState, player)
    
            # print current game state
            print_game_state(gameState)
            
            # evaluate game state
            if move_was_winning_move(gameState, player):
                winner.append(player)
                winnerEncoded.append(symbols[player])
                noWinnerYet = False
    
            # switch player and increase move counter
            player *= -1
            mvcntr +=  1
    
    
    
        if noWinnerYet:
            winner.append(0)
            winnerEncoded.append('draw')
            
    return winner, winnerEncoded


if __name__ == '__main__':
    
    times = 100
    winner, winnerEncoded = simulate(times)
    finalCount = collections.Counter(winner)
    
    plt.figure(1)
    plot_label = ['Draw','x','o']
    plt.bar([1,2,3],finalCount.values(), align="center")
    plt.xticks([1,2,3], plot_label)
    plt.suptitle('Count of Wins for each Player', fontsize=20)
    
    winOrDraw = {}
    winOrDraw['draw'] = finalCount[0]
    winOrDraw['win/loss'] = finalCount[1] + finalCount[-1]
    
    plt.figure(2)
    plot_label2 = ['Win or Loss', 'Draw']
    plt.bar([1,2],winOrDraw.values(), align="center")
    plt.xticks([1,2], plot_label2)
    plt.suptitle('Win/Loss vs Draw', fontsize=20)
    
    plt.show()
    
    #print(finalCount)
    #print(winOrDraw)
    

