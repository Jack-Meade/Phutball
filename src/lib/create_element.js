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
  if (type === 'th') { cell.scope = 'col' }
  return cell
}

function create_h2(innerHTML) {
  var h2       = document.createElement('h2')
  h2.innerHTML = innerHTML
  return h2
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
  var section, canvas, labels, data
  Array.from(graph_section.children).forEach(child => { child.remove() })
  labels = results.map((r, i) => { return `Experiment ${i+1}` })

  //////////////////////////////////////////////////

  section = create_section()
  section.style.width  = '1000px'
  section.style.height = '600px'
  section.appendChild(create_h2('Average Game Time'))
  canvas    = document.createElement('canvas')
  canvas.id = 'time-canvas'
  data      = {
    labels : labels,
    datasets : [{
      data            : results.map(result => { return result['time'] }),
      backgroundColor : gen_colours(results.length)
    }]
  },
  draw_graph(canvas, data, 'Experiment', 'Average Game Time').render()
  section.appendChild(canvas)
  graph_section.appendChild(section)

  //////////////////////////////////////////////////

  section = create_section()
  section.style.width  = '1000px'
  section.style.height = '600px'
  section.appendChild(create_h2('Average Turn Times'))
  canvas    = document.createElement('canvas')
  canvas.id = 'turn-canvas'
  data      = {
    labels : labels,
    datasets : get_turn_datasets(results)
  }
  draw_graph(canvas, data, 'Experiment', 'Average Turn Times').render()
  section.appendChild(canvas)
  graph_section.appendChild(section)
}

function draw_graph(ctx, data, xaxis_label, yaxis_label) {
  return new Chart(ctx, {
    type : 'bar',
    data : data,
    options : {
      responsive          : true,
      maintainAspectRatio : false,
      layout : {
        padding : { 
          top   : 20,
          right : 20
        }
      },
      legend : { display : false },
      scales : {
        xAxes : [{
          scaleLabel : {
            display : true,
            labelString : xaxis_label
          }
        }],
        yAxes : [{
          scaleLabel : {
            display : true,
            labelString : yaxis_label
          },
          ticks : {
            beginAtZero : true
          }
        }]
      }
    }
  })
}

function get_turn_datasets(results) {
  var p1 = []
  var p2 = []
  results.forEach(result => { 
    p1.push(result['p1-time'])
    p2.push(result['p2-time'])
  })

  return [{
      label           : 'Player1 Turn',
      backgroundColor : 'red',
      data            : p1
    }, {
      label           : 'Player2 Turn',
      backgroundColor : 'blue',
      data            : p2
    }
  ]
}
