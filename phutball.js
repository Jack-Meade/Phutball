(function() {

  document.addEventListener('DOMContentLoaded', init, false);

  const SPACING = 25;

  var canvas, ctx, board, player1_score, player2_score, error_msg;
  var placing_player = false;
  var kicking_ball   = false;

  function init() {
    canvas = document.querySelector("canvas");
    ctx    = canvas.getContext("2d");
    setup_listeners()

    send_request({ action : "init" })
    canvas.height = (board.length-1)*SPACING
    canvas.width  = (board[0].length-1)*SPACING

    draw_game(ctx);
  }

  function player_turn(x, y) {
    if (placing_player || kicking_ball) {
      x = Math.round(x / SPACING);
      y = Math.round(y / SPACING);
      send_request({ action : "player", x : x, y : y})
      draw_game();
    }
  }

  function send_request(req_params) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "", false);

    try {
      xhr.send(JSON.stringify({
        action    : req_params.action,
        x         : req_params.x,
        y         : req_params.y,
        kicking   : kicking_ball,
        num_turns : req_params.num_turns,
        ai_type   : document.querySelector('input[name="rad_ai"]:checked').value
      }));

      if (xhr.status != 200) {
        console.log(`Error ${xhr.status}: ${xhr.statusText}`);
      } else {
        var response  = JSON.parse(xhr.response);
        board         = response.board;
        player1_score = response.p1;
        player2_score = response.p2;
        error_msg     = response.error_msg || "";
      }
    } catch(err) {
      alert(`${err}\n${xhr.response}`);
    }
  }

  function draw_game() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    update_status();
    ctx.fillStyle = "#000000";

    var ball_coords;
    for (var y = 0; y < board.length; y++) {
      for (var x = 0; x < board[y].length; x++) {
        switch (board[y][x]) {
          case 3: case 4: case 5:
            draw_grid(x, y, ctx);
            break;
          case 2:
            draw_player(x, y, ctx);
            break;
          case 1:
            ball_coords = { x : x, y : y }
        }
      }
    }
    draw_ball(ball_coords.x, ball_coords.y, ctx);
  }

  function draw_grid(x, y) {
    ctx.moveTo(x*SPACING, y*SPACING - SPACING);
    ctx.lineTo(x*SPACING, y*SPACING + SPACING);
    ctx.stroke();

    ctx.moveTo(x*SPACING - SPACING, y*SPACING);
    ctx.lineTo(x*SPACING + SPACING, y*SPACING);
    ctx.stroke();
  }

  function draw_player(x, y) {
    ctx.fillStyle = "#000000";
    fill_circle(x, y);
    draw_grid(x, y, ctx);
  }

  function draw_ball(x, y) {
    draw_grid(x, y, ctx);
    ctx.fillStyle = "#FFFFFF";
    fill_circle(x, y);
    ctx.stroke();
    ctx.beginPath();
  }

  function fill_circle(x, y) {
    ctx.beginPath();
    ctx.arc(x*SPACING, y*SPACING, 10, 0, 2 * Math.PI);
    ctx.fill();
  }

  function update_status() {
    if      (placing_player) { document.getElementById('status').innerHTML = "Currently: Placing player"; }
    else if (kicking_ball)   { document.getElementById('status').innerHTML = "Currently: Kicking ball"; }
    else                     { document.getElementById('status').innerHTML = "Currently: Philosophising"; }
    document.getElementById('player1_score').innerHTML = "Player 1: " + player1_score;
    document.getElementById('player2_score').innerHTML = "Player 2: " + player2_score;
    document.getElementById('error_msg').innerHTML     = error_msg;
  }

  function setup_listeners() {
    document.getElementById("but_player").addEventListener('click', function() {
      if (!kicking_ball)   { placing_player = !placing_player; update_status(); }
    }, false);
    document.getElementById("but_kick").addEventListener('click', function() {
      if (!placing_player) { kicking_ball = !kicking_ball; update_status(); }
    }, false);
    document.getElementById("but_ai").addEventListener('click', function() {
      send_request({ action : "ai", num_turns : Math.floor(num_turns=document.getElementById("input_num_turns").value) });
      draw_game();
    }, false);

    canvas.addEventListener('click', function (e) {
      player_turn(e.offsetX, e.offsetY);
    }, false);
  }

})();
