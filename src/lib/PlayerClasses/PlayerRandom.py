from random  import randint
from .Player import Player

class PlayerRandom(Player):
    @staticmethod
    def take_turn(board, p1, depth, heuristic, abp):
        boards = board.get_successors()
        return boards.pop(randint(0, len(boards)-1))