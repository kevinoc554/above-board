$(document).ready(function () {
  disableOption()
  initMaterialize();
});

// Initializes all relevant JS for MaterializeCSS components
function initMaterialize() {
  $('.sidenav').sidenav();
  $('select').formSelect();
}

// Applies the 'disabled' property to the first option 
// in each of the dynamically created select elements
function disableOption() {
  $('#genre').children().first().prop('disabled', true);
  $('#mechanics').children().first().prop('disabled', true);
}
