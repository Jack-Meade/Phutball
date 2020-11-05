export function create_label(innerHTML, htmlFor) {
  var label       = document.createElement('label')
  label.htmlFor   = htmlFor
  label.innerHTML = innerHTML
  return label
}

export function create_input(type, id) {
  var input       = document.createElement('input')
  input.type      = type
  input.className = id
  input.name      = id
  input.required  = true
  return input
}

export function create_section() {
  var section = document.createElement('section')
  return section
}

export function create_select(id, options) {
  var select       = document.createElement('select')
  select.className = id
  select.name      = id
  options.forEach(option => {
    select.appendChild(create_option(option.innerHTML, option.value))
  })
  return select
}

function create_option(innerHTML, value) {
  var option       = document.createElement('option')
  option.innerHTML = innerHTML
  option.value     = value
  return option
}

export function create_button(innerHTML, type) {
  var button       = document.createElement('button')
  button.innerHTML = innerHTML
  button.type      = type
  return button
}


export function create_table(results) {
  var section = document.querySelector('#results-table')
  
  var previous_table = section.querySelector('table')
  if (previous_table) { previous_table.remove() }
  
  var table = document.createElement('table')
  table.appendChild(create_table_headers(results))
  
  for (var i = 0; i < results.length; i++) {
    table.appendChild(create_row(i, results[i]))
  }
  
  section.appendChild(table)
}

export function create_table_headers(results) {
  var row = document.createElement('tr')
  row.appendChild(create_cell('th', '#'))

  for (var key in results[0]) {
    row.appendChild(create_cell('th', key.toUpperCase()))
  }

  return row
}

export function create_row(exp_num, results) {
  var row = document.createElement('tr')
  
  row.appendChild(create_cell('td', exp_num))
  
  for (var key in results) {
    row.appendChild(create_cell('td', results[key]))
  }

  return row
}

export function create_cell(type, innerHTML) {
  var cell       = document.createElement(type)
  cell.innerHTML = innerHTML
  return cell
}

function gen_colours(num_results) {
  var colours = []
  for (var i=0; i < num_results; i++) {
    colours.push(`rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`)
  }
  return colours
}

export function create_graph(results) {
  var graph_section = document.querySelector('#results-graph')

  var time_canvas          = (document.querySelector('#time_canvas')) ? document.querySelector('#time_canvas') : document.createElement('canvas')
  time_canvas.id           = 'time_canvas'
  time_canvas.style.width  = "300px"
  time_canvas.style.height = "300px"

  var myChart = new Chart(time_canvas, {
    type : 'bar',
    data : {
      labels : results.map((r, i) => { return i+1 }),
      datasets : [{
        data  : results.map(result => { return result['time'] }),
        backgroundColor : gen_colours(results.length)
      }]
    },
    options : {
      title : 'Runtime',
      legend : { display : false },
      scales : {
        yAxes : [{
          ticks : {
            beginAtZero: true
          }
        }]
      }
    }
  }).render()

  graph_section.appendChild(time_canvas)
}

