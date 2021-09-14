$(document).ready(function () {
  disableOption();
  initMaterialize();
  toTopBtn();
});

// Initializes all relevant JS for MaterializeCSS components
function initMaterialize() {
  $('.sidenav').sidenav();
  $('select').formSelect();
  $('.modal').modal();
}

// Applies the 'disabled' property to the first option 
// in each of the dynamically created select elements
function disableOption() {
  $('#genre').children().first().prop('disabled', true);
  $('#mechanics').children().first().prop('disabled', true);
  $('#rating').children().first().prop('disabled', true);
  $('#weight').children().first().prop('disabled', true);
}

// Custom JS for Return to Top Button
// Button fades in and out on scroll
// On click, button scrolls smoothly to the top of the page
function toTopBtn() {
  $(window).scroll(function () {
    if ($(this).scrollTop() > 150) {
      $('#toTopBtn').fadeIn();
    } else {
      $('#toTopBtn').fadeOut();
    }
  });
  $('#toTopBtn').click(function () {
    $('html, body').stop().animate({
      scrollTop: 0
    }, 1000);
  });
  $('html, body').on('scroll mousedown DOMMouseScroll mousewheel keyup touchstart', function (e) {
    if (e.which > 0 || e.type === 'mousedown' || e.type === 'mousewheel' || e.type === 'touchstart') {
        $('html, body').stop();
    }
});
}