from abc  import ABC, abstractmethod
from copy import deepcopy

class Player(ABC):
    @abstractmethod
    def take_turn(self):
        pass

    @staticmethod
    def get_successes(board):
        boards  = Player.place_players(board)
        boards += Player.kick_ball(board)
        
        return boards

    @staticmethod
    def place_players(board):
        boards = []
        # for every cell, place player where applicable (not on player|ball) on a new_board
        for y in range(1, len(board.state)-1):
            for x in range(1, len(board.state[y])-1):
                new_board = deepcopy(board)

                if not new_board.is_player(x, y) and not new_board.is_ball(x, y):
                    new_board.update(x, y, "player")
                    boards.append(new_board)
        return boards

    @staticmethod
    def kick_ball(board):
        steps = [
            { "x" : -1, "y" : -1 },
            { "x" :  0, "y" : -1 },
            { "x" :  1, "y" : -1 },
            { "x" : -1, "y" :  0 },
            { "x" :  1, "y" :  0 },
            { "x" : -1, "y" :  1 },
            { "x" :  0, "y" :  1 },
            { "x" :  1, "y" :  1 }
        ]
        boards = []

        # for each cell next to ball, determine if you can kick in a line
        for step in steps:
            players = []
            curX    = board.ball["x"] + step["x"]
            curY    = board.ball["y"] + step["y"]

            # while there is a player along the line
            while board.is_player(curX, curY):
                players.append({ "x" : curX, "y" : curY })
                curX += step["x"]
                curY += step["y"]

            # if line ends on a wall, skip
            if board.is_wall(curX, curY): continue

            # if players were found, append board and update new_board ball coords
            if len(players):
                new_board = deepcopy(board)
                new_board.remove_players(players)
                new_board.update(curX, curY, "ball", { "x" : curX, "y" : curY })
                boards.append(new_board)
        return boards
    