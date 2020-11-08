function required(name) {
  throw new Error(`missing required parameter: ${name}`)
}

export function create_element({ elm=required('elm'),htmlFor=null,innerHTML=null,id=null,class_name=null,name=null,width=null,height=null,options=null,type=null } = {}) {
  var element = document.createElement(elm)
  if (class_name != null) { element.className    = class_name }
  if (id != null)         { element.id           = id }
  if (name != null)       { element.name         = name }
  if (innerHTML != null)  { element.innerHTML    = innerHTML }
  if (htmlFor != null)    { element.htmlFor      = htmlFor }
  if (width != null)      { element.style.width  = width }
  if (height != null)     { element.style.height = height }

  if (elm === 'input') { 
    element.type     = type
    element.required = true
  } else if (elm === 'select') {
    options.forEach(option => {
      element.appendChild(create_option(option.innerHTML, option.value))
    })
  } else if (elm === 'th') {
    element.scope = 'col'
  }

  return element
}

function create_option(innerHTML, value) {
  var option       = document.createElement('option')
  option.innerHTML = innerHTML
  option.value     = value
  return option
}

export function create_table(results) {
  var section = document.querySelector('#results-table')
  
  var previous_table = section.querySelector('table')
  if (previous_table) { previous_table.remove() }
  
  var table = document.createElement('table')
  table.appendChild(create_table_headers(results))
  
  for (var i = 0; i < results.length; i++) {
    table.appendChild(create_row(i+1, results[i]))
  }
  
  section.appendChild(table)
}

function create_table_headers(results) {
  var row = document.createElement('tr')
  row.appendChild(create_element({ elm : 'th', innerHTML : '#' }))

  for (var key in results[0]) {
    row.appendChild(create_element({ elm : 'th', innerHTML : key.toUpperCase() }))
  }

  return row
}

function create_row(exp_num, results) {
  var row = document.createElement('tr')
  
  row.appendChild(create_element({ elm : 'td', innerHTML : exp_num }))
  
  for (var key in results) {
    row.appendChild(create_element({ elm : 'td', innerHTML : results[key] }))
  }

  return row
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

  section   = create_element({ elm : 'section', width : '1000px', height : '600px' })
  section.appendChild(create_element({ elm : 'h2', innerHTML : 'Average Game Time'}))
  canvas    = create_element({ elm : 'canvas', id : 'time-canvas' })
  data      = {
    labels : labels,
    datasets : [{
      data            : results.map(result => { return result['time'] }),
      backgroundColor : gen_colours(results.length)
    }]
  },
  draw_graph(canvas, data, 'Experiment', 'Average Game Time (seconds)').render()
  section.appendChild(canvas)
  graph_section.appendChild(section)

  //////////////////////////////////////////////////

  section   = create_element({ elm : 'section', width : '1000px', height : '600px' })
  section.appendChild(create_element({ elm : 'h2', innerHTML : 'Average Turn Times'}))
  canvas    = create_element({ elm : 'canvas', id : 'turn-canvas' })
  data      = {
    labels : labels,
    datasets : get_player_datasets(results, { p1 : 'p1-time', p2 : 'p2-time' })
  }
  draw_graph(canvas, data, 'Experiment', 'Average Turn Times (seconds)').render()
  section.appendChild(canvas)
  graph_section.appendChild(section)

  //////////////////////////////////////////////////

  section   = create_element({ elm : 'section', width : '1000px', height : '600px' })
  section.appendChild(create_element({ elm : 'h2', innerHTML : 'Player Scores'}))
  canvas    = create_element({ elm : 'canvas', id : 'scores-canvas' })
  data      = {
    labels : labels,
    datasets : get_player_datasets(results, { p1 : 'player1', p2 : 'player2' })
  }
  draw_graph(canvas, data, 'Experiment', 'Score').render()
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

function get_player_datasets(results, keys) {
  var p1 = []
  var p2 = []
  results.forEach(result => { 
    p1.push(result[keys.p1])
    p2.push(result[keys.p2])
  })

  return [{
      label           : `Player1 ${ (keys.p1 === 'player1') ? 'score' : keys.p1.replace('p1-','')}`,
      backgroundColor : 'blue',
      data            : p1
    }, {
      label           : `Player2 ${ (keys.p2 === 'player2') ? 'score' : keys.p2.replace('p2-','')}`,
      backgroundColor : 'red',
      data            : p2
    }
  ]
}
