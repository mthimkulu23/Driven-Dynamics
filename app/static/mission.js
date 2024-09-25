
function goToLandingPage1( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/";

 }

function goToLandingPage3( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/signup";
 }

 function goToLandingPage4( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/login";
 }


 function goToLandingPage6( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/contact_us";
 }

 function goToLandingPage16( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/enquire";
 }


 function goToLandingPage17( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/landing";
 }


 function goToLandingPage18( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/catelog_buyer";
 }

 function goToLandingPage20( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/landing";
 }


 function goToLandingPage24( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/sell_review";
 }

 function goToLandingPage25( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/catelog_buyer";
 }


 function goToLandingPage28( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/review_display12";
 }



 function goToLandingPage90( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/seller_message";
 }


 function goToLandingPage50( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/catelog_buyer";
 }


 function goToLandingPage45( ) {
  // Replace the URL "/landing-page" with the actual URL or route of the landing page
 window.location.href = "https://driven-dynamics.onrender.com/catelog";
 }






let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("demo");
  let captionText = document.getElementById("caption");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  captionText.innerHTML = dots[slideIndex-1].alt;
}






















        
















