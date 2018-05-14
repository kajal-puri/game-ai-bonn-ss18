import numpy as np
import itertools
import matplotlib.pyplot as plt

PROB_MASS_FILE = 'prob_mass'
# load prob_mass
mass_distrib = np.array(np.loadtxt(PROB_MASS_FILE)).reshape(3, 3)

def move_still_possible(S):
    return not (S[S==0].size == 0)

def plot_confusion_matrix(cm):
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('confusion matrix');
    plt.colorbar()
    plt.yticks(np.arange(3), ['0', '1', '2'], rotation=90)
    plt.xticks(np.arange(3), ['0', '1', '2'])

    fmt = '.4f' if normalize else 'd'
thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def normalize(arr):
    # return arr / np.linalg.norm(arr)
    sum = np.sum(arr)
    arr /= sum
    return arr;

def move_based_on_prob_mass(S, p):
    xs, ys = np.where(S == 0)
    print mass_distrib[xs, ys]
    probs = normalize(mass_distrib[xs, ys])
    i = np.random.choice(len(probs), 1, p=probs)[0]
    S[xs[i], ys[i]] = p
    print xs[i], ys[i]
    return S

def move_at_random(S, p):
    xs, ys = np.where(S==0)
    i = np.random.permutation(np.arange(xs.size))[0]
    S[xs[i], ys[i]] = p
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
symbols = {1: 'x', -1: 'o', 0: ' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B

def run_game(first_player_strategy, second_player_strategy):
    # initialize 3x3 tic tac toe board
    gameState = np.zeros((3,3), dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True
    
    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        print '%s moves' % name

        # let player move at random
        
        gameState = first_player_strategy(gameState, player) if player == 1 else second_player_strategy(gameState, player)

        # print current game state
        print_game_state(gameState)
        
        # evaluate game state
        if move_was_winning_move(gameState, player):
            print 'player %s wins after %d moves' % (name, mvcntr)
            noWinnerYet = False
            return gameState, player

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1
        
    if noWinnerYet:
        return gameState, 0
        print 'game ended in a draw'

# calculate the probability mass function 
def calc_prob_mass(agg):
    return normalize(agg.flatten())

def simulate(times = 10):
    aggregate = np.zeros((3,3), dtype=float)
    scores = (0, 0, 0)
    count_random = 0
    
    for i in range(times):
        gameState, player = run_game(move_at_random, move_based_on_prob_mass)
        scores += np.array((player == 1, player == -1, player == 0), dtype=int)
        if player != 0:
            aggregate = np.add(aggregate, np.clip(gameState * player, 0, 1))
            if player == 1:
                count_random += 1
                
    return aggregate, scores

if __name__ == '__main__':
    times = 1000
    agg, scores = simulate(times)
    prob_mass = calc_prob_mass(agg)
    
    # np.random.choice(9, 1, p=prob_mass)[0]
    
    # print '%d games had winner.' % scores
    norm = normalize(agg)
    plt.figure('1')
    plot_confusion_matrix(norm)
    plt.figure('2')
    plot_confusion_matrix(agg)
    plt.show()
