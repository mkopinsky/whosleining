var $parshiot = $('#parshiot');
var $calendar_type = $('#calendar-type');

var yomtov;
var israel;

if ($('#yom-tov').prop('checked')) {
  yomtov = 'on';
} else {
  yomtov = 'off';
}

if ($calendar_type.val() === 'Israel') {
  israel = 'on';
} else {
  israel = 'off';
}

var hebcal = $.getJSON(
  'https://www.hebcal.com/hebcal/?v=1&cfg=json&year=now&month=x&s=on&maj=' + yomtov + '&i=' + israel
).done(function(data) {
  data.items.forEach(function(item) {
    $parshiot.append('<span>' + item.date + ' </span><span>' + item.hebrew + '</span></br>');
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
