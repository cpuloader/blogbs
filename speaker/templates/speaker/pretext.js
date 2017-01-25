$(document).ready(function() {

  var textField = document.getElementById('id_text_to_say')
  textField.style.color = "#BBBBBB";
  textField.addEventListener('click', function() {
    textField.innerHTML = "";
    textField.style.color = "black";
  }, false);

  if (window.location.href.indexOf('False') == -1) {
      document.getElementById('submit-btn').click();
  }
});