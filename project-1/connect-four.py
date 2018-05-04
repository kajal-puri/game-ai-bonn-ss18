import numpy as np


class Connect4:
    def __init__(self):
        self.gameState = np.zeros((3, 3), dtype=int)
        self.cap = self.gameState.shape[1]
        self.kmoves = np.zeros(self.gameState.shape[0])
        self.symbols = {1: 'x', -1: 'o', 0: ' '}

    def move_at(self, row, player):
        if self.kmoves[row] == self.cap:
            return self.gameState;
        filled = np.count_nonzero(self.gameState[row])
        self.gameState[row][filled] = player
        self.kmoves[row] += 1

    def possible_moves(self):
        return np.where(self.kmoves != self.cap)[0]
        
    def print_board(self):
        B = np.copy(self.gameState).astype(object)
        for n in [-1, 0, 1]:
            B[B==n] = self.symbols[n]
        print B

    def evaluate(self):
        return False
        # TODO 
        
    def play(players):
        player = 1
        mvcounter = 1

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

game.move_at(1, 1)
game.move_at(1, 1)
game.move_at(1, 1)
game.move_at(2, -1)
game.move_at(2, 1)
game.print_board();

# # def move_random(gameState, player):
# #     xs, ys = np.
