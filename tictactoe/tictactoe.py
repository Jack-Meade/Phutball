import numpy as np
from random import randint
from copy   import deepcopy
from json   import dumps, loads

class Board(object):
  def __init__(self):
    self.state = [" " for _ in range(9)]

  def __len__(self):
    return len(self.state)

  def reset(self):
    self.state = [" " for _ in range(9)]

  def available_moves(self):
    return [i for i in range(9) if self.state[i] == " "] if not self._game_over() else []

  def next_states(self, player):
    OPP = "o" if player == "x" else "x"
    
    opp_states = []
    for move, cell in enumerate(self.state):
      if cell == " ":
        new_board = deepcopy(self)
        new_board.move(move, OPP)
        opp_states.append(new_board)

    return opp_states

  def move(self, move, player):
    self.state[move] = player
    return self._game_over()

  def _game_over(self):
    lines = [(0,1,2), (0,3,6), (0,4,8), (1,4,7), (2,4,6), (2,5,8), (3,4,5), (6,7,8)]

    for line in lines:
      line = self.state[line[0]] + self.state[line[1]] + self.state[line[2]]
      
      if   line == "xxx": return "x"
      elif line == "ooo": return "o"

    if any(cell == " " for cell in self.state): return 0
    return "d"

  def display(self, player=None):
    if player:
      print(f"Player {player} takes turn:")
    print("|{}|{}|{}|".format(self.state[0], self.state[1], self.state[2]))
    print("|{}|{}|{}|".format(self.state[3], self.state[4], self.state[5]))
    print("|{}|{}|{}|".format(self.state[6], self.state[7], self.state[8]))
    

class PlayerRandom(object):
  def __init__(self, player, previous=None):
    self.qtable = []
    self.player = player

  def take_turn(self, board):
    moves = board.available_moves()
    return board.move(moves[randint(0, len(moves))-1], self.player)

  def update_last_action(self, qvalue):
    pass


class PlayerQL(object):
  def __init__(self, player, previous=None):
    self.player      = player
    self.epsilon     = 0.9
    self.greed       = 0.5
    self.last_action = (None, None)
    
    if previous: 
      with open(previous, "r") as file: self.qtable = loads(file.read())
    else:        
      self.qtable = {}

  def train(self, games, display):
    if self.player == "x": p1 = self; p2 = PlayerRandom("o")
    else:                  p2 = self; p1 = PlayerRandom("x")

    run(p1, p2, games, display)
    self.last_action = (None, None)

  def take_turn(self, board):
    state = "".join(board.state)
    if not state in self.qtable: self.qtable[state] = [0.0 for i in range(len(board))]

    qvalues = self.get_qvalues(board)
    if np.random.random() < self.greed:
      action, _ = max(qvalues, key=lambda elm: elm[1])

    else:
      good_actions = [action for action, qvalue in qvalues if qvalue != -1]

      if not len(good_actions):
        self.update_last_action(-1)
        action, _ = qvalues[randint(0, len(qvalues)-1)]

      else:
        action = good_actions[randint(0, len(good_actions)-1)]
      
    result = board.move(action, self.player)
    reward = self.determine_reward(result)

    max_nqvalue = 0
    for nboard in board.next_states(self.player):
      nstate = "".join(nboard.state)

      if not nstate in self.qtable: 
        self.qtable[nstate] = [0.0 for i in range(len(board))]

      nqvalues = self.get_qvalues(nboard)

      if not nqvalues:
        self.qtable[state][action] = float(reward)
        break
      else:
        _, nqvalue  = max(nqvalues, key=lambda elm: elm[1])
        max_nqvalue = max(max_nqvalue, nqvalue)

    self.qtable[state][action] = reward + self.epsilon * max_nqvalue
    self.last_action           = (state, action)

    return result

  def determine_reward(self, result):
    if   result in [self.player, "d"]: return 1
    elif result == 0:                  return 0
    return -1

  def update_last_action(self, qvalue):
    state, action = self.last_action
    
    self.qtable[state][action] = float(qvalue)
    self.last_action           = (None, None)

  def get_qvalues(self, board):
    state   = "".join(board.state)
    actions = board.available_moves()
    return [(action, qvalue) for action, qvalue in enumerate(self.qtable[state]) if action in actions] if len(actions) else None

class PlayerHuman(object):
  def __init__(self, player):
    self.player = player

  def take_turn(self, board):
    while True:
      try:
        row = int(input("Row: "))-1
        col = int(input("Col: "))-1

        if 0 > row or row > 2: raise ValueError
        if 0 > col or col > 2: raise ValueError

        action = row * 3 + col

        if action in board.available_moves(): break
        else:                                 print("Cannot place there")

      except ValueError:
        print("Input must be 1, 2, or 3")

    return board.move(action, self.player)

  def update_last_action(self, qvalue):
    pass


def run(p1, p2, games, display):
  board    = Board()
  score_p1 = 0
  score_p2 = 0
  draws    = 0

  human_player = any([isinstance(p1, PlayerHuman), isinstance(p2, PlayerHuman)])
  games_left   = games
  if human_player: board.display()

  while games_left:
    p1_result = p1.take_turn(board)
    if human_player: board.display(1)
    if   p1_result == "x":       
      board.reset(); games_left -= 1; score_p1 += 1; p2.update_last_action(-1)
      if human_player: board.display()
      continue
    elif p1_result == "d":
      board.reset(); games_left -= 1; draws += 1;    p2.update_last_action(1)
      if human_player: board.display()
      continue

    if human_player: print("-"*10)

    p2_result = p2.take_turn(board)
    if human_player: board.display(2)
    if   p2_result == "o":     
      board.reset(); games_left -= 1; score_p2 += 1; p1.update_last_action(-1)
      if human_player: board.display()
    elif p2_result == "d":
      board.reset(); games_left -= 1; draws += 1;    p1.update_last_action(1)
      if human_player: board.display()

    if human_player: print("-"*10)

  if display:
    per_p1 = round(score_p1 / games * 100, 2)
    per_p2 = round(score_p2 / games * 100, 2)
    per_dr = round(draws    / games * 100, 2)
    score_width = len(str(games))
    print(f"P1W: {per_p1:-6}% ({score_p1:{score_width}}/{games})\nP2W: {per_p2:-6}% ({score_p2:{score_width}}/{games})\nDRW: {per_dr:-6}% ({draws:{score_width}}/{games})")

  return p1, score_p1, p2, score_p2

def test(rounds, games, fresh=False, training=False):
  P1_JSON = "p1.json"
  P2_JSON = "p2.json"
  
  if fresh:
    p1 = PlayerQL("x")
    p2 = PlayerQL("o")
    if training:
      p1.train(games, False)
      p2.train(games, False)
  else:
    p1 = PlayerQL("x", P1_JSON)
    p2 = PlayerQL("o", P2_JSON)

  for i in range(rounds):
    print(f"----- (Round {i+1}) -----")
    run(p1, p2, games, True)
    print(f"----- (Round {i+1}) -----\n")

  if not fresh:
    with open(P1_JSON, "w") as file:
      file.write(dumps(p1.qtable))

    with open(P2_JSON, "w") as file:
      file.write(dumps(p2.qtable))

def play():
  p1 = None; p2 = None

  player = input("x or o: ")
  while not player in ["x", "o"]:
    player = input("x or o: ")

  if player == "x": p1 = PlayerHuman("x")
  else:             p2 = PlayerHuman("o")

  if p1: p2 = PlayerQL("o", "p2.json")
  else:  p1 = PlayerQL("x", "p1.json")

  while True:
    try:
      num_games = int(input("Number of games: "))

      if 1 > num_games or num_games > 100: raise ValueError
      break

    except ValueError:
      print("Number of games must between 1-100")
  
  run(p1, p2, num_games, True)
  

if __name__ == "__main__":
  test(20, 5000)
  # play()
