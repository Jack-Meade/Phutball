(function() {

  document.addEventListener('DOMContentLoaded', init, false);

  function init() {
    document.getElementById("play_options").style.display = "none";
    setup_listeners()
  }

  function setup_listeners() {
    document.getElementById("but_play").addEventListener('click', function() {
      play_options = document.getElementById("play_options");
    
      if (play_options.style.display == "none") { play_options.style.display = "block"; }
      else                                      { play_options.style.display = "none"; }
    }, false);

    document.getElementById("but_exp").addEventListener('click', function() {
       
    }, false);
  }
})();