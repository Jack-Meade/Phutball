from http.server              import SimpleHTTPRequestHandler
from socketserver             import TCPServer
from json                     import loads, dumps

from lib.Board                import Board
from lib.PlayerClasses        import PlayerRandom, PlayerMinimax, PlayerRL

class PhutballHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body           = loads(self.rfile.read(content_length))
        self.send_response(200)
        self.end_headers()

        if body["action"] == "init":
            self.server.restart()
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
        self._board      = Board(11, 7)
        self._p1_score   = 0
        self._p2_score   = 0
        self._p1_turn    = True
        self._error_msg  = ""
        self._ai         = {
            "PlayerRandom"  : PlayerRandom(),
            "PlayerMinimax" : PlayerMinimax(self._board),
            "PlayerRL"      : PlayerRL()
        }

        TCPServer.__init__(self, (addr[0], addr[1]), handler)

    def _get_board(self):
        return self._board.state
    def _get_p1_score(self):
        return self._p1_score
    def _get_p2_score(self):
        return self._p2_score
    def _get_error_msg(self):
        return self._error_msg

    board      = property(_get_board)
    p1         = property(_get_p1_score)
    p2         = property(_get_p2_score)
    error_msg  = property(_get_error_msg)

    # Start up server
    def start(self):
        self.serve_forever()

    def restart(self):
        self._board      = Board(11, 7)
        self._p1_score   = 0
        self._p2_score   = 0
        self._p1_turn    = True
        self._error_msg  = ""
        self._ai         = {
            "PlayerRandom"  : PlayerRandom(),
            "PlayerMinimax" : PlayerMinimax(self._board),
            "PlayerRL"      : PlayerRL()
        }

    # Determine if player move is legal
    def player_turn(self, x, y, kicking, ai_type):
        if not self._p1_turn: self._error_msg = "Please run the AI once more, you must be Player 1"; return
        self._error_msg = ""
        valid_turn      = False

        ##################################################
        if kicking:
            if self._board.is_wall(x, y): 
                self._error_msg = "You cannot put the ball offside, or kick it inplace!"

            elif self._board.is_goal(y):
                if self._board.kick_ball(x, y):
                    if y <= 1: self._p2_score += 1
                    else:      self._p1_score += 1
                    self._reset_board()

            elif self._board.is_player(x, y):
                self._error_msg = "Player already in that position!"

            else:
                valid_turn = self._board.kick_ball(x, y)
                if not valid_turn: self._error_msg = "Missing player to kick ball there!"
        ##################################################
        else:
            # if cell is wall or ball
            if self._board.is_wall(x, y):
                self._error_msg = "You cannot put a player on the side or ball!"

            # if cell is goal of player 1|2
            elif self._board.is_goal(y):
                # if cell is not back part of goal
                if y != 0 and y != len(self._board)-1:
                    self._board.update(x, y, "player")
                    valid_turn = True
                else:
                    self._error_msg = "You cannot put a player in goal!"

            # if cell already has player
            elif self._board.is_player(x, y):
                self._error_msg = "Player already in that position!"

            # else cell is empty
            else:
                self._board.update(x, y, "player")
                valid_turn = True
        ##################################################

        if valid_turn:
            self._ai_turn(ai_type, False)

    def run_ai(self, num_turns, ai_type):
        for _ in range(num_turns):
            game_over = self._ai_turn(ai_type, self._p1_turn)
            if not game_over:
                self._p1_turn = not self._p1_turn
            else:
                self._p1_turn = True          
                self._reset_board()
        self._error_msg = ""

    def _ai_turn(self, ai_type, player1):
        player    = self._ai[ai_type]
        new_board = player.take_turn(self._board, player1)

        if   new_board.ball["y"] <= 1:                  self._p2_score += 1; return True
        elif new_board.ball["y"] >= len(self._board)-2: self._p1_score += 1; return True
        else:                                         
            self._board = new_board
            return False

    def _reset_board(self):
        self._board.reset_board()
        self._ai["PlayerMinimax"] = PlayerMinimax(self._board)  


def run_server(port, handler):
    server_running = False
    while not server_running:
        try:
            httpd          = PhutballServer(("", port), handler)
            server_running = True
            print("Serving at http://localhost:{}/src/".format(port))
            httpd.start()
        except OSError:
            print("{} in use, trying next".format(port))
            port += 1

if __name__ == '__main__':
    handler = PhutballHandler
    port    = 8080
    run_server(port, handler)
