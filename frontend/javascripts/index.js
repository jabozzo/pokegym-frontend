String.prototype.capitalize = function() {
    return this.replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); });
};

$(document).ready(function() {
    moment.locale('es')
    setInterval(function() {
      update_date()
    }, 1000)
    update_date()
})

function update_date(){
    moment.locale('es')
    date = moment()
    day = date.format('D')
    month = date.format('MMMM').capitalize()
    $('#container_date').html(day + ' de ' + month)
}

function update_date_and_clock(){
    moment.locale('es')
    date = moment().format('LLLL')
    $('#date').html(date)
}
