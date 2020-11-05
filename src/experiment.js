import { create_label, create_input, create_section, create_select, create_button, create_table } from './lib/create_element.js'

(function() {

  document.addEventListener('DOMContentLoaded', init, false)

  var form
  
  function init() {
    setup_listeners()
    form = document.querySelector('form')
    add_exp()
  }

  function send_request() {
    var xhr = new XMLHttpRequest()
    xhr.open('POST', '', false)

    var experiments = get_form_data()

    if (!experiments) return
    
    try {
      xhr.send(JSON.stringify({
        action      : 'experiments',
        experiments : experiments
      }))

      if (xhr.status != 200) {
        console.log(`Error ${xhr.status}: ${xhr.statusText}`)
      } else {
        var response = JSON.parse(xhr.response)
        create_table(response.results)
        // create_graph(response.results)
        document.querySelector(".tab-buttons").click()
      }
    } catch(err) {
      alert(`${err}\n${xhr.response}`)
    }
  }

  function get_form_data() {
    var experiments = []

    var fieldsets_okay = Array.from(form.getElementsByTagName('fieldset')).every(fieldset => {
      var experiment = {}

      var sections_okay = Array.from(fieldset.getElementsByTagName('section')).every(section => {
        var inputs = Array.from(section.getElementsByTagName('input')).concat(Array.from(section.getElementsByTagName('select')))
    
        var inputs_okay = inputs.every(input => {
          if (input.value === '') { return false }
          
          experiment[[input.className]] = isNaN(input.value) ? input.value : Number(input.value)

          if (input.className === 'height' || input.className === 'width') { 
            if      (experiment[[input.className]] % 2 === 0) { return false }
            else if (experiment[[input.className]] < 4)       { return false }
          }
          return true
        })
        return inputs_okay
      })
      experiments.push(experiment)
      return sections_okay
    })

    return fieldsets_okay ? experiments : null
  }

  function add_exp() {
    var new_exp = document.createElement('fieldset')

    var section = create_section()

    section.appendChild(create_label('Height:', 'height'))
    section.appendChild(create_input('number', 'height'))

    section.appendChild(create_label('Width:', 'width'))
    section.appendChild(create_input('number', 'width'))

    section.appendChild(create_label('Games:', 'nofgames'))
    section.appendChild(create_input('number', 'nofgames'))

    new_exp.appendChild(section)

    section = create_section()    
    section.appendChild(create_label('Player 1:', 'player1'))
    var select = create_select('player1', [
      { 'innerHTML' : 'Random',    'value' : 'PlayerRandom' },
      { 'innerHTML' : 'Minimax',   'value' : 'PlayerMinimax' },
      { 'innerHTML' : 'Rlearning', 'value' : 'PlayerRL' }
    ])
    select.onchange = is_minimax
    section.appendChild(select)
    new_exp.appendChild(section)

    section = create_section()
    section.appendChild(create_label('Player 2:', 'player2'))
    select = create_select('player2', [
      { 'innerHTML' : 'Random',    'value' : 'PlayerRandom' },
      { 'innerHTML' : 'Minimax',   'value' : 'PlayerMinimax' },
      { 'innerHTML' : 'Rlearning', 'value' : 'PlayerRL' }
    ])
    select.onchange = is_minimax
    section.appendChild(select)
    new_exp.appendChild(section)

    var button = create_button('Delete', 'button')
    button.onclick = del_exp
    new_exp.appendChild(button)

    form.appendChild(new_exp)
  }

  function del_exp(e) {
    e.target.parentNode.remove()
  }

  function is_minimax(e) {
    var node   = e.target
    var index  = Array.prototype.indexOf.call(node.parentNode.children, node)
    var player = node.parentNode.children[0].htmlFor.replace('layer', '')

    if (node.value === 'PlayerMinimax') {
      node.parentNode.insertBefore(create_select(`${player}-heuristic`, [
        { 'innerHTML' : 'Heuristic1',    'value' : 'heuristic1' },
        { 'innerHTML' : 'Heuristic2',    'value' : 'heuristic2' },
        { 'innerHTML' : 'Heuristic3',    'value' : 'heuristic3' },
      ]), node.parentNode.children[index+1])
      node.parentNode.insertBefore(create_label(`${player.toUpperCase()} Heuristic:`, `${player}-heuristic`), node.parentNode.children[index+1])
      node.parentNode.insertBefore(create_input('number', `${player}-depth`), node.parentNode.children[index+1])
      node.parentNode.insertBefore(create_label(`${player.toUpperCase()} Depth:`, `${player}-depth`), node.parentNode.children[index+1])
      node.mini_options_added = true

    } else if (node.mini_options_added) {
      node.parentNode.children[index+1].remove()
      node.parentNode.children[index+1].remove()
      node.parentNode.children[index+1].remove()
      node.parentNode.children[index+1].remove()
      node.mini_options_added = false
    }
  }

  function open_tab(e) {
    document.querySelectorAll(".results-tab").forEach(tab_content => {
      tab_content.style.display = "none";
    })

    document.querySelectorAll(".tab-buttons").forEach(tab_button => {
      tab_button.className = tab_button.className.replace(" active", "");
    })

    document.getElementById('results-'+e.target.innerHTML.toLowerCase()).style.display = "block";
    e.target.className += " active";
    }

  function setup_listeners() {
    document.getElementById('add').addEventListener('click', add_exp, false)

    document.querySelector('button[type="submit"]').addEventListener('click', function(e) {
      send_request()
      e.preventDefault()
    }, false)

    Array.from(document.querySelectorAll('.tab-buttons')).forEach(tab_button => {
      tab_button.addEventListener('click', open_tab, false)
    })
  }
})()