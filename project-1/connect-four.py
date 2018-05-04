import numpy as np

class Connect4:
    def __init__(self):
        self.state = np.zeros((4, 4), dtype=int)
        self.cap = self.state.shape[1]
        self.kmoves = np.zeros(self.state.shape[0])
        self.symbols = {1: 'x', -1: 'o', 0: ' '}

    def move_at(self, row, player):
        if self.kmoves[row] == self.cap:
            return self.state;
        filled = np.count_nonzero(self.state[row])
        self.state[row][filled] = player
        self.kmoves[row] += 1

    def possible_moves(self):
        return np.where(self.kmoves != self.cap)[0]
        
    def print_board(self):
        B = np.copy(self.state).astype(object)
        for n in [-1, 0, 1]:
            B[B==n] = self.symbols[n]
        print B

    def eval(self, player):
        boundX, boundY = self.state.shape
        for x in range(boundX):
            for y in range(boundY):
                if x - 3 > -1 and len(np.where(self.state[x - 3:4, y] == player)[0]) == 4: # |
                    return True
                elif y + 3 < boundY and len(np.where(self.state[x, y:4] == player)[0]) == 4: # _
                    return True
                else:
                    arr = np.array([])
                    if x - 3 > -1 and y + 3 < boundY: # /
                        arr = np.array([self.state[x][y], self.state[x -1, y + 1], self.state[x - 2, y + 2], self.state[x - 3, y + 3]])
                    elif x + 3 < boundX and y + 3 < boundY: # \
                        arr = np.array([self.state[x][y], self.state[x + 1, y + 1], self.state[x + 2, y + 2], self.state[x + 3, y + 3]])
                    if (len(np.where(arr == player)[0]) == 4):
                        return True
                
        return False
        
    def play(players):
        # init player and counter
        player = 1
        mvcounter = 1

        # flag used to stop the gmae once someone won
        noWinnerYet = True
        
        while len(self.possible_moves()) != 0 and noWinnerYet:
            move = players[1 if player == 1 else 0].next()
            self.move_at(move, player)
            noWinnerYet = self.evaluate()
            player *= -1
            mvcounter += 1

game = Connect4();

class RandomPlayer:
    def next(self, game):
        return np.random.choice(game.possible_moves(), 1)[0]

game.move_at(2, 1)
game.move_at(2, -1)
game.move_at(2, 1)
game.move_at(1, -1)
game.move_at(1, 1)
game.move_at(1, -1)

game.move_at(0, 1)
game.move_at(0, -1)
game.move_at(0, -1)
game.move_at(0, -1)
game.move_at(3, -1)

game.print_board();
print game.eval(1)
print game.eval(-1)
