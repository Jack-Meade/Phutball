from .Player import Player
from ..Node  import Node


class PlayerMinimax(Player):
    @staticmethod
    def take_turn(board, player1):
        DEPTH = 3

        root       = Node(board)
        root       = PlayerMinimax._build_tree(root, DEPTH)
        root.value = PlayerMinimax._minimax(root, DEPTH, float('-inf'), float('inf'), player1)
        fav_child  = max(root.children) if player1 else min(root.children)
    
        return fav_child.board

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
            return PlayerMinimax._heuristic(node.board)

        else:
            highlow = float('-inf') if player1 else float('inf')

            for child in node.children:
                child.value = PlayerMinimax._minimax(child, depth-1, alpha, beta, not player1)

                if player1: highlow = max(highlow, child.value); alpha = max(alpha, child.value)
                else:       highlow = min(highlow, child.value); beta  = min(beta,  child.value)

                # if beta <= alpha: break

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
                    elif y >= len(board)-1: score += 10000
                    else:
                        if   y < len(board)//2: score -= 10 * y
                        elif y > len(board)//2: score += 10 * y

        return score