from PlayerClasses.Player import Player

class PlayerRandom(Player):
    @staticmethod
    def take_turn(board, ball):
        return board, ball