from abc  import ABC, abstractmethod
from copy import deepcopy

class Player(ABC):
    @abstractmethod
    def take_turn(self, board, ball, p1):
        pass

    @staticmethod
    def get_successes(board, ball):
        boards = Player.place_players(board, ball)
        boards += Player.kick_ball(board, ball)
        
        return boards

    @staticmethod
    def place_players(board, ball):
        boards = []
        # for every cell, place player where applicable (not on player|ball) on a new_board
        for y in range(1, len(board)-1):
            for x in range(1, len(board[y])-1):
                new_board = deepcopy(board)

                if not new_board[y][x] in [1,2]:
                    new_board[y][x] = 2
                    boards.append({
                        "board" : new_board,
                        "ball"  : ball,
                    })
        return boards

    @staticmethod
    def kick_ball(board, ball):
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
            curX    = ball["x"] + step["x"]
            curY    = ball["y"] + step["y"]

            # while there is a player along the line
            while board[curY][curX] == 2:
                players.append({ "x" : curX, "y" : curY })
                curX += step["x"]
                curY += step["y"]

            # if line ends on a wall, skip
            if board[curY][curX] == 0: continue

            # if players were found, append board and update new_board ball coords
            if len(players):
                new_board = deepcopy(board)
                Player.remove_players(new_board, players)
                new_board[ball["y"]][ball["x"]] = 5
                new_board[curY][curX]           = 1
                boards.append({
                    "board" : new_board,
                    "ball"  : { "x" : curX, "y" : curY },
                })
        return boards

    @staticmethod
    def remove_players(board, players):
        for player in players:
            if   player["y"] == 1:            board[player["y"]][player["x"]] = 3
            elif player["y"] == len(board)-2: board[player["y"]][player["x"]] = 4
            else:                             board[player["y"]][player["x"]] = 5
    