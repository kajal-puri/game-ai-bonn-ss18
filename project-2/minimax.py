# Enumerate players
MAX = 1
MIN = -1

def mean(numbers):
  return float(sum(numbers)) / max(len(numbers), 1)

class Utility:
  # Utility values: mini: Minimax tree, maxi: Maximax tree, avgi: Average Tree,
  # idx: In case of draw, the node with lower idx is preferred (n2 is more
  # preferable than n3).
  def __init__(self, mini, maxi=None, avgi=None):
    self.mini = mini
    self.maxi = mini if maxi is None else maxi
    self.avgi = mini if avgi is None else avgi

  def __str__(self):
    return str((self.mini, self.maxi, self.avgi))

class Node:
  def __init__(self, idx, u=-1):
    self.name =  "n" + str(idx)
    self.utility = Utility(u)
    self.successors = []

  def is_terminal(self):
    return (len(self.successors) == 0)

  def add_successors(self, n):
    return self.successors.extend(n)

  def print_to_screen(self):
    if self.is_terminal():
      print self.utility
    else:
      [n.print_to_screen() for n in self.successors]


def mmv(s, p=MAX):
  if s.is_terminal():
    return s.utility

  if p==MAX:
    s.utility.mini = max([mmv(n, MIN) for n in s.successors], key=lambda x: x.mini).mini
    return s.utility
  else:
    s.utility.mini = min([mmv(n, MAX) for n in s.successors], key=lambda x: x.mini).mini
    return s.utility


def modified_mmv(s, p=MAX):
  if s.is_terminal():
    return s.utility

  if p==MAX:
    next_utilities = [modified_mmv(n, MIN) for n in s.successors]
    s.utility.mini = max(next_utilities, key=lambda x: x.mini).mini
    s.utility.maxi = max(next_utilities, key=lambda x: x.maxi).maxi
    s.utility.avgi = mean([n.utility.avgi for n in s.successors])
    return s.utility
  else:
    next_utilities = [modified_mmv(n, MAX) for n in s.successors]
    s.utility.mini = min(next_utilities, key=lambda x: x.mini).mini
    s.utility.maxi = max(next_utilities, key=lambda x: x.maxi).maxi
    s.utility.avgi = mean([n.utility.avgi for n in s.successors])
    return s.utility


if __name__ == '__main__':
  leaves = [15, 20, 1, 3, 3, 4, 15, 10, 16, 4, 12, 15, 12, 8]

  root_node = Node(0)
  level_1_nodes = [Node(i+1) for i in range(5)]
  level_2_nodes = [Node(i+6, leaves[i]) for i in range(len(leaves))]

  level_1_nodes[0].add_successors(level_2_nodes[0:4])
  level_1_nodes[1].add_successors(level_2_nodes[4:6])
  level_1_nodes[2].add_successors(level_2_nodes[6:8])
  level_1_nodes[3].add_successors(level_2_nodes[8:11])
  level_1_nodes[4].add_successors(level_2_nodes[11:14])
  root_node.add_successors(level_1_nodes)
  
  game_1_result = mmv(root_node)
  game_1_result_next_move = [n.name for n in level_1_nodes if n.utility.mini == game_1_result.mini]

  print "Game 1 result: " + str(game_1_result.mini) + ", Next move is: " + game_1_result_next_move[0]

  leaves = [18, 6, 16, 6, 5, 7, 1, 16, 16, 5, 10, 2]

  root_node = Node(0)
  level_1_nodes = [Node(i+1) for i in range(4)]
  level_2_nodes = [Node(i+5, leaves[i]) for i in range(len(leaves))]

  level_1_nodes[0].add_successors(level_2_nodes[0:5])
  level_1_nodes[1].add_successors(level_2_nodes[5:7])
  level_1_nodes[2].add_successors(level_2_nodes[7:10])
  level_1_nodes[3].add_successors(level_2_nodes[10:12])
  root_node.add_successors(level_1_nodes)
  
  game_2_result = mmv(root_node)
  game_2_result_next_move = [n.name for n in level_1_nodes if n.utility.mini == game_2_result.mini]

  print "Game 2 result: " + str(game_2_result.mini) + ", Next move is: " + game_2_result_next_move[0]

  modified_game_2_result = modified_mmv(root_node)
  modified_game_2_result_next_move = [n for n in level_1_nodes if n.utility.mini == modified_game_2_result.mini]

  if len(modified_game_2_result_next_move) > 1:
    modified_game_2_result_next_move = [n for n in modified_game_2_result_next_move if n.utility.maxi == modified_game_2_result.maxi]

  if len(modified_game_2_result_next_move) > 1:
    modified_game_2_result_next_move = [n for n in modified_game_2_result_next_move if n.utility.avgi == modified_game_2_result.avgi]

  print "Modified Game 2 result: " + str(modified_game_2_result) + ", Next move is: " + modified_game_2_result_next_move[0].name

