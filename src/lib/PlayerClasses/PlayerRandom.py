from random  import randint
from .Player import Player

class PlayerRandom(Player):
    @staticmethod
    def take_turn(board, p1):
        boards = Player.get_successes(board)
        return boards.pop(randint(0, len(boards)-1))