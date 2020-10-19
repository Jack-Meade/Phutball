from http.server  import SimpleHTTPRequestHandler
from socketserver import TCPServer
from json         import loads, dumps

from random       import randint
from copy         import deepcopy

class PhutballHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = loads(self.rfile.read(content_length))
        self.send_response(200)
        self.end_headers()

        if body["action"] == "init":
            self.send_game_state()

        elif body["action"] == "player":
            self.server.player_turn(body["x"], body["y"], body["kicking"], body["ai_type"])
            self.send_game_state()

        elif body["action"] == "ai":
            self.server.run_ai(body["num_turns"], body["ai_type"])
            self.send_game_state()


    def send_game_state(self):
        self.wfile.write(bytes(dumps({
            "board"     : self.server.board,
            "p1"        : self.server.p1,
            "p2"        : self.server.p2,
            "error_msg" : self.server.error_msg
        }), encoding='utf8'))

class PhutballServer(TCPServer):
    def __init__(self, addr, handler):
        # self._board = [
        #     [3,3,3,3,3,3,3],
        #     [0,3,3,3,3,3,0],#1
        #     [0,5,5,5,5,5,0],#2
        #     [0,5,5,5,5,5,0],#3
        #     [0,5,5,5,5,5,0],#4
        #     [0,5,5,1,5,5,0],#5
        #     [0,5,5,5,5,5,0],#6
        #     [0,5,5,5,5,5,0],#7
        #     [0,5,5,5,5,5,0],#8
        #     [0,4,4,4,4,4,0],#9
        #     [4,4,4,4,4,4,4]
        # ]
        # self._ball_coords = { "x" : 3, "y" : 5 }
        self._board = [
            [3,3,3,3,3],
            [0,3,3,3,0],
            [0,5,1,5,0],
            [0,4,4,4,0],
            [4,4,4,4,4]
        ]
        self._ball_coords = { "x" : 2, "y" : 2 }

        self._reset_copy  = (deepcopy(self._board), deepcopy(self._ball_coords))
        self._p1_score    = 0
        self._p2_score    = 0
        self._p1_turn     = True
        self._error_msg   = ""

        TCPServer.__init__(self, (addr[0], addr[1]), handler)

    def _get_board(self):
        return self._board
    def _get_p1_score(self):
        return self._p1_score
    def _get_p2_score(self):
        return self._p2_score
    def _get_ai_running(self):
        return self._ai_running
    def _set_ai_running(self, state):
        self._ai_running = state
    def _get_error_msg(self):
        return self._error_msg

    board      = property(_get_board)
    p1         = property(_get_p1_score)
    p2         = property(_get_p2_score)
    ai_running = property(_get_ai_running, _set_ai_running)
    error_msg  = property(_get_error_msg)

    # Start up server
    def start(self):
        self.serve_forever()

    # Determine if player move is legal
    def player_turn(self, x, y, kicking, ai_type):
        self._error_msg = ""
        valid_turn      = False

        # if cell is wall or ball
        if self._board[y][x] in [0, 1]:
            if kicking: self._error_msg = "You cannot put the ball offside, or kick it inplace!"
            else:       self._error_msg = "You cannot put a player on the side or ball!"

        # if cell is goal of player 1|2
        elif self._board[y][x] in [3, 4]:
            if kicking:
                if self._kick_ball(x, y):
                    if y <= 1: self._p2_score += 1
                    else:      self._p1_score += 1
                    self._reset_board()
            else:
                # if cell is not back part of goal
                if y != 0 and y != len(self._board)-1:
                    self._board[y][x] = 2
                    valid_turn        = True
                else:
                    self._error_msg = "You cannot put a player in goal!"

        # if cell already has player
        elif self._board[y][x] == 2:
            self._error_msg = "Player already in that position!"

        # else cell is empty
        else:
            if kicking:
                valid_turn = self._kick_ball(x, y)
            else:
                self._board[y][x] = 2
                valid_turn        = True

        if valid_turn:
            self._ai_turn(ai_type, False)

    def _kick_ball(self, newX, newY):
        stepX   = 0
        stepY   = 0
        players = []

        # if cell is one away from ball (no player inbetween)
        if abs(newX - self._ball_coords["x"]) == 1 or abs(newY - self._ball_coords["y"]) == 1:
            self._error_msg = "Missing player to kick ball there!"
            return False

        # Determine if cell is above/below and left/right of ball,
        #  otherwise it is on the same axis
        if   newX < self._ball_coords["x"]: stepX = -1
        elif newX > self._ball_coords["x"]: stepX =  1

        if   newY < self._ball_coords["y"]: stepY = -1
        elif newY > self._ball_coords["y"]: stepY =  1

        curX = self._ball_coords["x"]
        curY = self._ball_coords["y"]

        # while we haven't reached the new cell
        while curX != newX or curY != newY:
            curX += stepX
            curY += stepY

            if curX == newX and curY == newY: continue

            # if there is no player along line to new cell
            if self._board[curY][curX] != 2:
                self._error_msg = "Missing player to kick ball there!"
                return False
            players.append({ "x" : curX, "y" : curY })

        self._remove_players(self._board, players)

        self._board[self._ball_coords["y"]][self._ball_coords["x"]] = 5
        self._board[newY][newX]                                     = 1
        self._ball_coords                                           = { "x" : newX, "y" : newY }
        return True

    @staticmethod
    def _get_all_moves(board, ball_coords):
        steps = [
            { "x" : -1, "y" : -1 },
            { "x" : -1, "y" :  0 },
            { "x" : -1, "y" :  1 },
            { "x" :  0, "y" : -1 },
            { "x" :  0, "y" :  1 },
            { "x" :  1, "y" : -1 },
            { "x" :  1, "y" :  0 },
            { "x" :  1, "y" :  1 }
        ]
        boards = []

        # for every cell, place player where applicable (not on player|ball) on a new_board
        for y in range(1, len(board)-1):
            for x in range(1, len(board[y])-1):
                new_board = deepcopy(board)

                if not new_board[y][x] in [1,2]:
                    new_board[y][x] = 2
                    boards.append({
                        "board" : new_board,
                        "ball"  : ball_coords,
                    })

        # for each cell next to ball, determine if you can kick in a line
        for step in steps:
            players = []
            curX    = ball_coords["x"] + step["x"]
            curY    = ball_coords["y"] + step["y"]

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
                PhutballServer._remove_players(new_board, players)
                new_board[ball_coords["y"]][ball_coords["x"]] = 5
                new_board[curY][curX]                         = 1
                boards.append({
                    "board" : new_board,
                    "ball"  : { "x" : curX, "y" : curY },
                })
        return boards

    def _check_ai_scored(self, board, ball):
        if   ball["y"] <= 1:            self._p2_score += 1; self._reset_board()
        elif ball["y"] >= len(board)-1: self._p1_score += 1; self._reset_board()
        else:
            self._board       = deepcopy(board)
            self._ball_coords = deepcopy(ball)

    def run_ai(self, num_turns, ai_type):
        for _ in range(num_turns):
            self._ai_turn(ai_type)
            self._p1_turn = not self._p1_turn

    def _ai_turn(self, ai_type, p1=None):
        if p1 is None: p1 = self._p1_turn

        if ai_type == "random":
                self._ai_random()

        elif ai_type == "minimax":
            self._ai_minimax({
                "board"     : self._board,
                "ball"      : self._ball_coords,
            }, 3, float('-inf'), float('inf'), p1)

        elif ai_type == "rlearning":
            self._ai_rlearning()

    def _ai_random(self):
        boards       = self._get_all_moves(self._board, self._ball_coords)
        picked_board = boards.pop(randint(0, len(boards)-1))

        self._check_ai_scored(picked_board["board"], picked_board["ball"])

    def _ai_minimax(self, board, depth, alpha, beta, player1):
        move = self._build_tree(board, depth, alpha, beta, player1)
        print(move[0])
        self._check_ai_scored(move[1]["board"], move[1]["ball"])

    @staticmethod
    def _build_tree(board, depth, alpha, beta, player1):
        if depth == 0 or board["ball"]["y"] <= 1 or board["ball"]["y"] >= len(board["board"][0])-1:
            return PhutballServer._heuristic(board["board"]), board

        if player1:
            highest = float('-inf')
            for move in PhutballServer._get_all_moves(board["board"], board["ball"]):
                cur_move = PhutballServer._build_tree(move, depth-1, alpha, beta, False)
                highest  = max(highest, cur_move[0])
                alpha    = max(alpha,   cur_move[0])

                if beta <= alpha: break
            return highest, move

        else:
            lowest = float('inf')
            for move in PhutballServer._get_all_moves(board["board"], board["ball"]):
                cur_move = PhutballServer._build_tree(move, depth-1, alpha, beta, True)
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

    def _ai_rlearning(self):
        print("rlearning")

    @staticmethod
    def _remove_players(board, players):
        for player in players:
            if   player["y"] == 1:            board[player["y"]][player["x"]] = 3
            elif player["y"] == len(board)-2: board[player["y"]][player["x"]] = 4
            else:                             board[player["y"]][player["x"]] = 5

    def _reset_board(self):
        self._board       = deepcopy(self._reset_copy[0])
        self._ball_coords = deepcopy(self._reset_copy[1])

    def print_board(self):
        print()
        print("Player1: {}\nPlayer2: {}".format(self._p1_score, self._p2_score))
        for row in self._board:
            colstr = ""
            for col in row:
                colstr += "|{}".format(col)
            colstr += "|"
            print(colstr)

def run_server(port, handler):
    server_running = False
    while not server_running:
        try:
            httpd          = PhutballServer(("", port), handler)
            server_running = True
            print("Serving at http://localhost:{}".format(port))
            httpd.start()
        except OSError:
            print("{} in use, trying next".format(port))
            port += 1

def test1(port, handler):
    server = PhutballServer(("", port), handler)
    with open("results.txt", "a") as file:
        for i in range(100):
            print("Test #{}".format(i))
            server.run_ai(10000, "random")
            file.write("Player 1: {}\nPlayer 2: {}\n\n".format(server.p1, server.p2))
        print("Finished")

if __name__ == '__main__':
    handler = PhutballHandler
    port    = 8080
    run_server(port, handler)
    # test1(port, handler)
