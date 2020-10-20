from http.server          import SimpleHTTPRequestHandler
from socketserver         import TCPServer
from json                 import loads, dumps
    
from random               import randint
from copy                 import deepcopy
from importlib            import import_module
from PlayerClasses.Player import Player

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
        self._board = [
            [3,3,3,3,3,3,3],
            [0,3,3,3,3,3,0],#1
            [0,5,5,5,5,5,0],#2
            [0,5,5,5,5,5,0],#3
            [0,5,5,5,5,5,0],#4
            [0,5,5,1,5,5,0],#5
            [0,5,5,5,5,5,0],#6
            [0,5,5,5,5,5,0],#7
            [0,5,5,5,5,5,0],#8
            [0,4,4,4,4,4,0],#9
            [4,4,4,4,4,4,4]
        ]
        self._ball = { "x" : 3, "y" : 5 }
        # self._board = [
        #     [3,3,3,3,3],
        #     [0,3,3,3,0],
        #     [0,5,1,5,0],
        #     [0,4,4,4,0],
        #     [4,4,4,4,4]
        # ]
        # self._ball = { "x" : 2, "y" : 2 }

        self._reset_copy = (deepcopy(self._board), deepcopy(self._ball))
        self._p1_score   = 0
        self._p2_score   = 0
        self._p1_turn    = True
        self._error_msg  = ""

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
        if abs(newX - self._ball["x"]) == 1 or abs(newY - self._ball["y"]) == 1:
            self._error_msg = "Missing player to kick ball there!"
            return False

        # Determine if cell is above/below and left/right of ball,
        #  otherwise it is on the same axis
        if   newX < self._ball["x"]: stepX = -1
        elif newX > self._ball["x"]: stepX =  1

        if   newY < self._ball["y"]: stepY = -1
        elif newY > self._ball["y"]: stepY =  1

        curX = self._ball["x"]
        curY = self._ball["y"]

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

        Player.remove_players(self._board, players)

        self._board[self._ball["y"]][self._ball["x"]] = 5
        self._board[newY][newX]                       = 1
        self._ball                                    = { "x" : newX, "y" : newY }
        return True

    def run_ai(self, num_turns, ai_type):
        for _ in range(num_turns):
            self._ai_turn(ai_type)
            self._p1_turn = not self._p1_turn

    def _ai_turn(self, ai_type, p1=None):
        if p1 is None: p1 = self._p1_turn

        player = getattr(import_module("PlayerClasses."+ai_type), ai_type)
        move   = player.take_turn(self._board, self._ball, self._p1_turn)

        if   move["ball"]["y"] <= 1:                  self._p2_score += 1; self._reset_board()
        elif move["ball"]["y"] >= len(self._board)-2: self._p1_score += 1; self._reset_board()
        else:                                         
            self._board, self._ball = move["board"], move["ball"]


    def _reset_board(self):
        self._board, self._ball = deepcopy(self._reset_copy[0]), deepcopy(self._reset_copy[1])

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
