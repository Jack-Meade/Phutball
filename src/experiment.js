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
    xhr.open("POST", "", false)

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
      }
    } catch(err) {
      alert(`${err}\n${xhr.response}`)
    }
  }

  function get_form_data() {
    var experiments = []
    var i           = 0
    var fieldset    = document.querySelector('fieldset')
    var num_inputs  = fieldset.getElementsByTagName('input').length + fieldset.getElementsByTagName('select').length
    
    for (var [key, value] of new FormData(form).entries()) { 
      if (i % num_inputs == 0) {
        experiment = {}
        experiments.push(experiment)
      }
      if (value == '') return false
      
      switch (true) {
        case key === "height": case key === "width":
          value = Number(value)
          if (value % 2 == 0) { return false }
          break

        case key === "nofgames":
          value = Number(value)
      }

      experiment[[key]] = value
      i++
    }
    return experiments
  }

  function add_exp() {
    var new_exp = document.createElement('fieldset')

    new_exp.appendChild(create_label('Height:', 'height'))
    new_exp.appendChild(create_input('number', 'height'))

    new_exp.appendChild(create_label('Width:', 'width'))
    new_exp.appendChild(create_input('number', 'width'))

    new_exp.appendChild(create_label('Games:', 'nofgames'))
    new_exp.appendChild(create_input('number', 'nofgames'))

    new_exp.appendChild(create_label('Player 1:', 'player1'))
    new_exp.appendChild(create_select('player1'))

    new_exp.appendChild(create_label('Player 2:', 'player2'))
    new_exp.appendChild(create_select('player2'))

    new_exp.appendChild(create_button('Delete', 'button'))

    form.appendChild(new_exp)
  }

  function create_label(innerHTML, htmlFor) {
    var element       = document.createElement('label')
    element.htmlFor   = htmlFor
    element.innerHTML = innerHTML
    return element
  }

  function create_input(type, id) {
    var element      = document.createElement('input')
    element.type     = type
    element.id       = id
    element.name     = id
    element.required = true
    return element
  }

  function create_select(id) {
    var element  = document.createElement('select')
    element.id   = id
    element.name = id
    element.appendChild(create_option('Random', 'PlayerRandom'))
    element.appendChild(create_option('Minimax', 'PlayerMinimax'))
    element.appendChild(create_option('Rlearning', 'PlayerRL'))
    return element
  }

  function create_option(innerHTML, value) {
    var element       = document.createElement('option')
    element.innerHTML = innerHTML
    element.value     = value
    return element
  }

  function create_button(innerHTML, type) {
    var element       = document.createElement('button')
    element.innerHTML = innerHTML
    element.type      = type
    element.addEventListener('click', del_exp, false)
    return element
  }

  function del_exp(e) {
    e.target.parentNode.remove()
  }

  function create_table(results) {
    var section = document.querySelector('#results-table')

    var previous_table = section.querySelector('table')
    if (previous_table) { previous_table.remove() }
    
    var table = document.createElement('table')
    table.appendChild(create_table_headers(results))

    for (var i = 0; i < results.length; i++) {
      row = create_row(i, results[i])
      table.appendChild(row)
    }

    section.appendChild(table)
  }

  function create_table_headers(results) {
    var row = document.createElement('tr')
    row.appendChild(create_cell('th', '#'))

    for (var key in results[0]) {
      row.appendChild(create_cell('th', key.toUpperCase()))
    }

    return row
  }
  
  function create_row(exp_num, results) {
    var row = document.createElement('tr')
    
    row.appendChild(create_cell('td', exp_num))
    
    for (var key in results) {
      row.appendChild(create_cell('td', results[key]))
    }

    return row
  }

  function create_cell(type, innerHTML) {
    var cell       = document.createElement(type)
    cell.innerHTML = innerHTML
    return cell
  }

  function setup_listeners() {
    document.getElementById('add').addEventListener('click', add_exp, false)

    document.querySelector("button[type='submit']").addEventListener('click', function(e) {
      send_request()
      e.preventDefault()
    }, false)
  }
})()