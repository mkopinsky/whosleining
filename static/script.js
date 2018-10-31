// disable hidden inputs for checkboxes when checked so that only the checked value gets passed to server
$('#submit').click(function() {
  if ($('#yom-tov').prop('checked')) {
    $('#yom-tov-hidden').prop('disabled', true);
  }
})
