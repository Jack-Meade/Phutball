from http.server              import SimpleHTTPRequestHandler
from socketserver             import TCPServer
from json                     import loads, dumps

from time                     import time
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

        elif body["action"] == "experiments":
            self.server.run_ai(body["experiments"])
            self.send_results()


    def send_game_state(self):
        self.wfile.write(bytes(dumps({
            "board"     : self.server.board,
            "p1"        : self.server.p1,
            "p2"        : self.server.p2,
            "error_msg" : self.server.error_msg
        }), encoding='utf8'))

    def send_results(self):
        self.wfile.write(bytes(dumps({
            "results" : self.server.results
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
        self._results    = []

        TCPServer.__init__(self, (addr[0], addr[1]), handler)

    def _get_board(self):
        return self._board.state
    def _get_p1_score(self):
        return self._p1_score
    def _get_p2_score(self):
        return self._p2_score
    def _get_error_msg(self):
        return self._error_msg
    def _get_results(self):
        return self._results

    board      = property(_get_board)
    p1         = property(_get_p1_score)
    p2         = property(_get_p2_score)
    error_msg  = property(_get_error_msg)
    results    = property(_get_results)

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
        self._results    = []

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

    def _ai_turn(self, ai_type, player1):
        player    = self._ai[ai_type]
        new_board = player.take_turn(self._board, player1, 3, "heuristic1")

        if   new_board.ball["y"] <= 1:                  self._p2_score += 1; self._reset_board(); return True
        elif new_board.ball["y"] >= len(self._board)-2: self._p1_score += 1; self._reset_board(); return True
        else:                                         
            self._board = new_board
            return False

    def run_ai(self, params):
        self._results = []
        num_e = len(str(len(params)))
        for i, experiment in enumerate(params):
            num_g      = len(str(experiment["nofgames"]))
            board      = Board(experiment["height"], experiment["width"])
            games_left = experiment["nofgames"]

            ai_types = {
                "PlayerRandom"  : PlayerRandom(),
                "PlayerMinimax" : PlayerMinimax(board),
                "PlayerRL"      : PlayerRL()
            }

            self._results.append({
                "time"         : 0,
                "height"       : experiment["height"],
                "width"        : experiment["width"],
                "games"        : experiment["nofgames"],
                "player1"      : 0,
                "player2"      : 0,
                "p1-type"      : experiment["player1"].replace("Player", ""),
                "p1-depth"     : experiment["p1-depth"]             if "p1-depth"     in experiment else None,
                "p1-heuristic" : experiment["p1-heuristic"].title() if "p1-heuristic" in experiment else None,
                "p1-time"      : 0,
                "p2-type"      : experiment["player2"].replace("Player", ""),
                "p2-depth"     : experiment["p2-depth"]             if "p2-depth"     in experiment else None,
                "p2-heuristic" : experiment["p2-heuristic"].title() if "p2-heuristic" in experiment else None,
                "p2-time"      : 0
            })

            turns = 0
            game_time = time()
            while games_left:
                player    = ai_types[experiment["player1"]] if self._p1_turn else ai_types[experiment["player2"]]
                depth     = self._determine_params(experiment, "p1-depth"     if self._p1_turn else "p2-depth")
                heuristic = self._determine_params(experiment, "p1-heuristic" if self._p1_turn else "p2-heuristic")

                turn_time  = time()
                result     = self._ai_turn_exp(board, player, self._p1_turn, depth, heuristic)
                end_time   = time() - turn_time
                turns     += 1

                if self._p1_turn: self._results[i]["p1-time"] += end_time
                else:             self._results[i]["p2-time"] += end_time

                if isinstance(result, Board):
                    self._p1_turn = not self._p1_turn
                    board         = result

                else:
                    end_time                  = time() - game_time
                    self._results[i]["time"] += end_time
                    self._results[i][result] += 1

                    self._p1_turn  = True          
                    games_left    -= 1
                    board.reset_board()
                    ai_types["PlayerMinimax"] = PlayerMinimax(board)
                    print("Experiment {0:{num_e}}: {1:{num_g}}/{2:{num_g}}".format(
                        i+1, (experiment["nofgames"]-games_left), experiment["nofgames"], num_e=num_e, num_g=num_g)
                    )
                    game_time = time()

            self._results[i]["time"]    = round(self.results[i]["time"] / experiment["nofgames"], 6)
            self._results[i]["p1-time"] = round(self._results[i]["p1-time"] / turns, 6)
            self._results[i]["p2-time"] = round(self._results[i]["p2-time"] / (turns if turns % 2 == 0 else turns-1), 6)

    def _ai_turn_exp(self, board, player, player1, depth, heuristic):
        new_board = player.take_turn(board, player1, depth, heuristic)

        if   new_board.ball["y"] <= 1:            self._p2_score += 1; return "player2"
        elif new_board.ball["y"] >= len(board)-2: self._p1_score += 1; return "player1"
        else:                                         
            board = new_board
            return board

    def _determine_params(self, experiment, key):
        if key in experiment: return experiment[key]
        return None

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
