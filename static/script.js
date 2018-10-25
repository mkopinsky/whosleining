// disable hidden inputs for checkboxes when checked so that only the checked value gets passed to server
$('#submit').click(function() {
  if ($('#shabbos').prop('checked')) {
    $('#shabbos-hidden').prop('disabled', true);
  }

  if ($('#yom-tov').prop('checked')) {
    $('#yom-tov-hidden').prop('disabled', true);
  }
})
