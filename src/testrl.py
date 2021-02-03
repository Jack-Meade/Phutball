from lib.PlayerClasses.PlayerRL import PlayerRL
from lib.Board                  import Board

b = Board(5, 5)
p = PlayerRL(b)
# p.train(b)
b = p.take_turn(b, True, None, None, None)
for row in b.state:
  print(row)

print("Placing player in [1,2]")
b.state[1][1] = 2
b = p.take_turn(b, True, None, None, None)
for row in b.state:
  print(row)
