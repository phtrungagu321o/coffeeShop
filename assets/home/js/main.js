// When the dashboard scrolls down 20px from the top of the document, slide down the navbar
window.onscroll = function () {
    scrollFunction()
};
const heightNav = document.getElementById("sticky").style.top;

function scrollFunction() {
    if (document.body.scrollTop > 30 || document.documentElement.scrollTop > 30) {
        document.getElementById("sticky").style.top = "0";
    } else {
        document.getElementById("sticky").style.top = heightNav;
    }
}

const video = document.getElementById("video-bg");

// Get the button
const btn = document.getElementById("status-Btn");

// Pause and play the video, and change the button text
function clickStatus() {
    if (video.paused) {
        video.play();
        btn.innerHTML = "Dừng Video";
    } else {
        video.pause();
        btn.innerHTML = "Phát Video";
    }
}

//opacity video
let videoWrap = document.querySelector('.header__wrap-video')
window.addEventListener('scroll', function () {
    let value = 1 + window.scrollY / -600;
    videoWrap.style.opacity = value;
})

// service
const topImg = document.querySelector('.imgBox__image');

function imgSlider(anything, topI) {
    document.querySelector('.imgBox__image').src = anything;
    topImg.style.top = topI
}

function changeCircleColor(color) {
    const circle = document.querySelector('.circle')
    circle.style.background = color
}

function changeText(textTitle, text) {
    document.getElementById('container__content-texBox--title').innerHTML = textTitle;

    document.getElementById('container__content-texBox--text').innerHTML = text;
}

$(function() {
  $( "#button" ).click(function() {
    $( "#button" ).addClass( "onclic", 250, validate);
  });

  function validate() {
    setTimeout(function() {
      $( "#button" ).removeClass( "onclic" );
      $( "#button" ).addClass( "validate", 450, callback );
    }, 2250 );
  }
    function callback() {
      setTimeout(function() {
        $( "#button" ).removeClass( "validate" );
      }, 1250 );
    }
  });
