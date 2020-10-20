from random               import randint
from PlayerClasses.Player import Player

class PlayerRandom(Player):
    @staticmethod
    def take_turn(board, ball, p1):
        boards = Player.get_successes(board, ball)
        return boards.pop(randint(0, len(boards)-1))