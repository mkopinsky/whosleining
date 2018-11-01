// disable hidden inputs for checkboxes when checked so that only the checked value gets passed to server
$('#submit').click(function() {
  if ($('#major').prop('checked')) {
    $('#major-hidden').prop('disabled', true);
  }
})
