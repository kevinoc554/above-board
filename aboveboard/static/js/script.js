//jshint esversion: 6

$(document).ready(function () {
  disableOption();
  initMaterialize();
  toTopBtn();
  closeFlashes();
  setRatingStars();
  showRateBtn();
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
  $('#genre').children().first().prop('disabled', true).attr('value', '');
  $('#mechanics').children().first().prop('disabled', true).attr('value', '');
  $('#rating').children().first().prop('disabled', true).attr('value', '');
  $('#weight').children().first().prop('disabled', true).attr('value', '');
}

// Return to Top Button
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

// Set the checked property on the correct star radio button
// based on average of ratings passed through route
function setRatingStars() {
  if ($('#rating-avg').length) {
    let avgRating = $('#rating-avg').text();
    $("input[value~=" + avgRating + "]").prop("checked", true);
  }
}

// Show button to submit ratings when user clicks on the star rating fieldset
function showRateBtn() {
  $('body').on('click', '#star-rating', function () {
    $('.rate-btn').slideDown('fast');
  });
}

// Close Flashed messages by clicking the X icon
function closeFlashes() {
  $('#close-flashes').on('click', function () {
    $('#flashes-row').slideUp();
  });
}