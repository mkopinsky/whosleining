var $parshiot = $('#parshiot');
var $calendar_type = $('#calendar-type');

var yomtov;
var israel;

$(function() {
  if (yt === 'on') {
    yomtov = 'on';
  } else {
    yomtov = 'off';
  }
})

$(function() {
  if (cal === 'Israel') {
    israel = 'on';
  } else {
    israel = 'off';
  }
})


var hebcal = $.getJSON(
  'https://www.hebcal.com/hebcal/?v=1&cfg=json&year=now&month=x&s=on&maj=' + yomtov + '&i=' + israel
).done(function(data) {
  var today = new Date();
  today.setHours(0, 0, 0, 0);
  data.items.forEach(function(item) {
    // format hebcal dates in order to compare each date to today's date
    var item_date_parts = item.date.split('-');
    var new_date = new Date(item_date_parts[0], item_date_parts[1]-1,   item_date_parts[2]);
    new_date.setHours(0, 0, 0, 0);
    // if the given date is today or later, display the date
    if (new_date >= today) {
      $parshiot.append('<span>' + item.date + ' </span><span>' + item.hebrew + '</span></br>');
    }
  })
}).fail(function(error) {
  return 'The parshiot data could not be loaded';
})

// disable hidden inputs for checkboxes when checked so that only the checked value gets passed to server
$('#submit').click(function() {
  if ($('#yom-tov').prop('checked')) {
    $('#yom-tov-hidden').prop('disabled', true);
  }
})
