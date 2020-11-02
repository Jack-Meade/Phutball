from copy    import deepcopy
from .Player import Player
from ..Node  import Node
from ..Board import Board

class PlayerMinimax(Player):
    def __init__(self, board):
        self._root = Node(Board(deepcopy(board.state)))

    def take_turn(self, board, player1):
        # If player makes move, find the child/move picked
        if board != self._root.board: self._root = self._find_child(board)

        self._root.value = PlayerMinimax._minimax(self._root, 3, float('-inf'), float('inf'), player1)
        self._root       = max(self._root.children) if player1 else min(self._root.children)

        return deepcopy(self._root.board)

    def _find_child(self, board):
        if len(self._root.children):
            for child in self._root.children:
                if child.board == board: return child
        
        else: # Only the very first move will have no children, generate them if this is the case
            self._root.children = [Node(cboard) for cboard in Player.get_successes(self._root.board)]
            return self._find_child(board)

    @staticmethod
    def _build_tree(node, depth):
        if depth == 0 or node.is_terminal():
            return node

        else:
            node.children = [Node(cboard) for cboard in Player.get_successes(node.board)]

            for child in node.children:
                child = PlayerMinimax._build_tree(child, depth-1)
                
            return node

    @staticmethod
    def _minimax(node, depth, alpha, beta, player1):
        if depth == 0 or node.is_terminal():
            return node.value or PlayerMinimax._heuristic(node.board)

        else:
            highlow       = float('-inf') if player1            else float('inf')
            node.children = node.children if len(node.children) else [Node(cboard) for cboard in Player.get_successes(node.board)]

            for child in node.children:
                child.value = PlayerMinimax._minimax(child, depth-1, alpha, beta, not player1)

                if player1: highlow = max(highlow, child.value); alpha = max(alpha, child.value)
                else:       highlow = min(highlow, child.value); beta  = min(beta,  child.value)

                if beta <= alpha: break

            return highlow

    @staticmethod
    def _heuristic(board):
        score = 0
        for y in range(len(board)):
            for x in range(len(board.state[y])):
                if board.is_player(x, y):
                    if   y < len(board)//2: score -= 1
                    elif y > len(board)//2: score += 1

                elif board.is_ball(x, y):
                    if   y <= 1:            score -= 10000
                    elif y >= len(board)-2: score += 10000
                    else:
                        if   y < len(board)//2: score -= 10 * y
                        elif y > len(board)//2: score += 10 * y

        return score
