// Configuration from backend/config.py
var base_address = 'http://localhost:4040';

$(document).ready(function(){
  add_pokemons_to_list();

  setInterval(function() {
    add_pokemons_to_list()
  }, 1000)
});

function add_pokemons_to_list() {
  var address = base_address + '/last'
  $.getJSON(address, function(data) {
    $('#table_pokemons tbody').empty()
    for(var i=0;i<data.length;i++){
      $('#table_pokemons tbody').append(
          '<tr><td><div class="col-1">' + data[i].id + '</div></td><td><div class="col-11">' + data[i].name + '</div></td></tr>'
      )
    }
  });
}
