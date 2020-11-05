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

export function create_select(id, options) {
  var select       = document.createElement('select')
  select.className = id
  select.name      = id
  options.forEach(option => {
    select.appendChild(create_option(option.innerHTML, option.value))
  })
  return select
}

export function create_option(innerHTML, value) {
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