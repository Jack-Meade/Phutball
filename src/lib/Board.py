from enum                  import Enum
from copy                  import deepcopy

class Board(object):
    def __init__(self, height, width):
        self._types = {
            "player" : 2,
            "p1goal" : 3,
            "p2goal" : 4,
            "empty"  : 5
        }
        self._board, self._ball = Board._gen_board(height, width)

        self._reset_copy = (deepcopy(self._board), deepcopy(self._ball))

    def __len__(self):
        return len(self._board)

    def __eq__(self, other):
        if type(other) == dict:
            return self._board == other["board"]
        return self._board == other.state

    def _get_board(self):
        return self._board
    def _get_ball(self):
        return self._ball

    state = property(_get_board)
    ball  = property(_get_ball)

    def kick_ball(self, newX, newY):
        stepX   = 0
        stepY   = 0
        players = []

        # if cell is one away from ball (no player in-between)
        if abs(newX - self._ball["x"]) == 1 or abs(newY - self._ball["y"]) == 1:
            return False

        # Determine if cell is above/below and left/right of ball,
        #  otherwise it is on the same axis
        if   newX < self._ball["x"]: stepX = -1
        elif newX > self._ball["x"]: stepX =  1

        if   newY < self._ball["y"]: stepY = -1
        elif newY > self._ball["y"]: stepY =  1

        curX = self._ball["x"] + stepX
        curY = self._ball["y"] + stepY

        # while we haven't reached the new cell
        while curX != newX or curY != newY:
            # if there is no player along line to new cell
            if not self.is_player(curX, curY):
                return False

            players.append({ "x" : curX, "y" : curY })
            curX += stepX
            curY += stepY

        self.remove_players(players)

        self.update(newX, newY, "ball", { "x" : newX, "y" : newY })
        return True

    def remove_players(self, players):
        for player in players:
            if   player["y"] == 1:           self.update(player["x"], player["y"], "p1goal")
            elif player["y"] == len(self)-2: self.update(player["x"], player["y"], "p2goal")
            else:                            self.update(player["x"], player["y"], "empty")

    def update(self, x, y, new_type, ball=None):
        if new_type == "ball":
            self._board[self._ball["y"]][self._ball["x"]] = 5
            self._board[y][x]                             = 1
            self._ball                                    = ball
        else:
            self._board[y][x] = self._types[new_type]

    def is_goal(self, y):
        return y <= 1 or y >= len(self._board)-2

    def is_ball(self, x, y):
        return self._ball["x"] == x and self._ball["y"] == y

    def is_wall(self, x, y):
        return self._board[y][x] == 0

    def is_player(self, x, y):
        return self._board[y][x] == 2

    def reset_board(self):
        self._board, self._ball = deepcopy(self._reset_copy[0]), deepcopy(self._reset_copy[1])

    @staticmethod
    def _gen_board(height, width):
        board = []
        ball  = { "x" : width//2, "y" : height//2 }

        for y in range(height):
            if   y == 0:          
                board.append([3 for _ in range(width)])

            elif y == 1:
                board.append([3 for _ in range(width)])
                board[-1][0]        = 0
                board[-1][width-1]  = 0

            elif y == height-1:   
                board.append([4 for _ in range(width)])

            elif y == height-2:
                board.append([4 for _ in range(width)])
                board[-1][0]        = 0
                board[-1][width-1]  = 0

            elif y == height//2:
                board.append([5 for _ in range(width)])
                board[-1][0]        = 0
                board[-1][width-1]  = 0
                board[-1][width//2] = 1

            else:
                board.append([5 for _ in range(width)])
                board[-1][0]        = 0
                board[-1][width-1]  = 0

        return board, ball

