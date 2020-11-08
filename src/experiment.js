import { create_element, create_table, create_graph } from './lib/create_element.js'

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
    xhr.ontimeout = () => { console.log('timed out :(') }

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
        create_graph(response.results)
        document.querySelectorAll(".tab-buttons")[1].click()
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

          } else if (input.className === 'nofgames' || input.className.includes('depth')) {
            if      (experiment[[input.className]] < 1)       { return false }

          } else if (input.className.includes('abp')) {
            experiment[[input.className]] = input.checked
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
    var new_exp = create_element({ elm : 'fieldset' })

    var section = create_element({ elm : 'section' })

    section.appendChild(create_element({ elm : 'label', innerHTML : 'Height:', htmlFor : 'height' }))
    section.appendChild(create_element({ elm : 'input', type : 'number', class_name : 'height' }))

    section.appendChild(create_element({ elm : 'label', innerHTML : 'Width:', htmlFor : 'width' }))
    section.appendChild(create_element({ elm : 'input', type : 'number', class_name : 'width' }))

    section.appendChild(create_element({ elm : 'label', innerHTML : 'Games:', htmlFor : 'nofgames' }))
    section.appendChild(create_element({ elm : 'input', type : 'number', class_name : 'nofgames' }))

    new_exp.appendChild(section)

    section = create_element({ elm : 'section' })  
    section.appendChild(create_element({ elm : 'label', innerHTML : 'Player 1:', htmlFor : 'player1'}))
    var select = create_element({ elm : 'select', class_name : 'player1', options : [
      { innerHTML : 'Random',    value : 'PlayerRandom' },
      { innerHTML : 'Minimax',   value : 'PlayerMinimax' },
      { innerHTML : 'Rlearning', value : 'PlayerRL' }
    ]})
    select.onchange = is_minimax
    section.appendChild(select)
    new_exp.appendChild(section)

    section = create_element({ elm : 'section' })
    section.appendChild(create_element({ elm : 'label', innerHTML : 'Player 2:', htmlFor : 'player2'}))
    select = create_element({ elm : 'select', class_name : 'player2', options : [
      { innerHTML : 'Random',    value : 'PlayerRandom' },
      { innerHTML : 'Minimax',   value : 'PlayerMinimax' },
      { innerHTML : 'Rlearning', value : 'PlayerRL' }
    ]})
    select.onchange = is_minimax
    section.appendChild(select)
    new_exp.appendChild(section)

    var button = create_element({ elm : 'button', innerHTML : 'Delete', type : 'button'})
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
      node.parentNode.insertBefore(create_element({ elm : 'input', type : 'checkbox', class_name : `${player}-abp`, value : `${player}-abp`, rinput : false }), node.parentNode.children[index+1])
      node.parentNode.insertBefore(create_element({ elm : 'label', innerHTML : `${player.toUpperCase()} AB-P:`, htmlFor : `${player}-abp` }), node.parentNode.children[index+1])
      node.parentNode.insertBefore(create_element({ elm : 'select', class_name : `${player}-heuristic`,  options : [
        { innerHTML : 'Heuristic1', value : 'heuristic1' },
        { innerHTML : 'Heuristic2', value : 'heuristic2' },
        { innerHTML : 'Heuristic3', value : 'heuristic3' },
      ]}), node.parentNode.children[index+1])
      node.parentNode.insertBefore(create_element({ elm : 'label', innerHTML : `${player.toUpperCase()} Heuristic:`, htmlFor : `${player}-heuristic` }), node.parentNode.children[index+1])
      node.parentNode.insertBefore(create_element({ elm : 'input', type : 'number', class_name : `${player}-depth` }), node.parentNode.children[index+1])
      node.parentNode.insertBefore(create_element({ elm : 'label', innerHTML : `${player.toUpperCase()} Depth:`, htmlFor : `${player}-depth` }), node.parentNode.children[index+1])
      node.mini_options_added = true

    } else if (node.mini_options_added) {
      node.parentNode.children[index+1].remove()
      node.parentNode.children[index+1].remove()
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