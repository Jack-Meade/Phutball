from PlayerClasses.Player import Player

class PlayerMinimax(Player):
    @staticmethod
    def take_turn(board, ball, p1):
        return PlayerMinimax._minimax({ "board" : board, "ball" : ball }, 3, float('-inf'), float('inf'), p1)[1]

    @staticmethod
    def _minimax(board, depth, alpha, beta, player1):
        return PlayerMinimax._build_tree(board, depth, alpha, beta, player1)

    @staticmethod
    def _build_tree(board, depth, alpha, beta, player1):
        if depth == 0 or board["ball"]["y"] <= 1 or board["ball"]["y"] >= len(board["board"][0])-1:
            return PlayerMinimax._heuristic(board["board"]), board

        if player1:
            highest = float('-inf')
            for move in Player.get_successes(board["board"], board["ball"]):
                cur_move = PlayerMinimax._build_tree(move, depth-1, alpha, beta, False)
                highest  = max(highest, cur_move[0])
                alpha    = max(alpha,   cur_move[0])

                if beta <= alpha: break
            return highest, move

        else:
            lowest = float('inf')
            for move in Player.get_successes(board["board"], board["ball"]):
                cur_move = PlayerMinimax._build_tree(move, depth-1, alpha, beta, True)
                lowest   = min(lowest, cur_move[0])
                beta     = min(beta,   cur_move[0])

                if beta <= alpha: break
            return lowest, move

    @staticmethod
    def _heuristic(board):
        score = 0
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == 2:
                    if   y < len(board)//2: score -= 1
                    elif y > len(board)//2: score += 1

                elif board[y][x] == 1:
                    if   y <= 1:            return -1000
                    elif y >= len(board)-1: return 1000
                    else:
                        if   y < len(board)//2: score -= 10 * y
                        elif y > len(board)//2: score += 10 * y

        return score