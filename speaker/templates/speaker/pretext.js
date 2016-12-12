$(document).ready(function() {

  var textField = document.getElementById('id_text_to_say')

  textField.addEventListener('click', function() {
    textField.innerHTML = "";
  }, false);

});