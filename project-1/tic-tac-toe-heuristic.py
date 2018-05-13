import numpy as np
import matplotlib.pyplot as plt

CUTOFF_DEPTH = 1
GAMES_COUNT = 1000

def move_still_possible(S):
  return not (S[S==0].size == 0)


def explore(S, p, depth=1):
  if depth == CUTOFF_DEPTH or not move_still_possible(S):
    return evaluate_game_state(S, p * -1)

  currentEvaluation = -10
  xs, ys = np.where(S==0)
  for i in np.arange(xs.size):
    gameState = np.copy(S).astype(object)
    gameState[xs[i],ys[i]] = p
    gameEvaluation = explore(gameState, p * -1, depth+1)
    if gameEvaluation > currentEvaluation:
      currentEvaluation = gameEvaluation
      educatedMove = np.copy(gameState).astype(object)
  return currentEvaluation

def move_educated(S, p):
  currentEvaluation = -10
  xs, ys = np.where(S==0)
  for i in np.arange(xs.size):
    gameState = np.copy(S).astype(object)
    gameState[xs[i],ys[i]] = p
    gameEvaluation = explore(gameState, p * -1)
    if gameEvaluation > currentEvaluation:
      currentEvaluation = gameEvaluation
      educatedMove = np.copy(gameState).astype(object)
  return educatedMove

    

def move_at_random(S, p):
  xs, ys = np.where(S==0)

  i = np.random.permutation(np.arange(xs.size))[0]
  
  S[xs[i],ys[i]] = p

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

def evaluate_game_state(S, p):
  evaluation = 0

  evaluation += np.sum(np.min(S * p, axis=0) != -1)

  evaluation += np.sum(np.min(S * p, axis=1) != -1)

  evaluation += (np.min(np.diag(S) * p) != -1)

  evaluation += (np.min(np.diag(np.rot90(S)) * p) != -1)

  evaluation -= np.sum(np.min(S * -p, axis=0) != -1)

  evaluation -= np.sum(np.min(S * -p, axis=1) != -1)

  evaluation -= (np.min(np.diag(S) * -p) != -1)

  evaluation -= (np.min(np.diag(np.rot90(S)) * -p) != -1)

  return evaluation


# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
  B = np.copy(S).astype(object)
  for n in [-1, 0, 1]:
    B[B==n] = symbols[n]
  print B


def play_game():
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

    # let player O move at random
    if player == -1:
      gameState = move_at_random(gameState, player)
    else:
      gameState = move_educated(gameState, player)

    # print current game state
    print_game_state(gameState)
    
    # evaluate game state
    if move_was_winning_move(gameState, player):
      print 'player %s wins after %d moves' % (name, mvcntr)
      noWinnerYet = False

    # switch player and increase move counter
    player *= -1
    mvcntr +=  1

  if noWinnerYet:
    print 'game ended in a draw'

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
  plt.title('Heuristic strategy for tic-tac-toe')
  plt.grid(True, axis='y')
  plt.show()
