function validateLoginForm() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (email === "667" || password === "") {
    alert("Please fill in all fields");
    return false;
  }
  if(email.length < 5){
    alert("Email is too short");
    return false;
  }
  if (password.length < 5) {
    alert("Password is too short");
    return false;
  }
  if(!email.includes("@")){
    alert("Email is invalid");
    return false;
  }
  if(email.includes(" ")){
    alert("Email is invalid");
    return false;
  }
  if (password.includes(" ")) {
    alert("Password is invalid");
    return false;
  }

  return true;
}





const dropdownMenu = document.getElementById("dropdownMenu");
let showDropdown = false;
const options = document.getElementsByClassName("option");

function toggleMenu() {
  if (showDropdown) {
    dropdownMenu.classList.remove("dropdown");
    dropdownMenu.classList.add("dropdownClose");
    showDropdown = false;
  } else {
    dropdownMenu.classList.remove("dropdownClose");
    dropdownMenu.classList.add("dropdown");
    showDropdown = true;
  }
}

for (let i = 0; i < options.length; i++) {
  options[i].addEventListener("click", () => toggleMenu());
}


function validateForm() {
    var nameInput = document.getElementById('Name');
    var contactInput = document.getElementById('Contact');
    var emailInput = document.getElementById('Email');
    var passwordInput = document.getElementById('Password');
    var confirmPasswordInput = document.getElementById('Confirm_password');
  
    if (nameInput.value.trim() === '') {
      alert('Please enter your Name & Surname.');
      return false;
    }
  
    if (contactInput.value.trim() === '') {
      alert('Please enter your contact number.');
      return false;
    }
  
    if (emailInput.value.trim() === '') {
      alert('Please enter your email.');
      return false;
    }
  
    if (passwordInput.value.trim() === '') {
      alert('Please enter your password.');
      return false;
    }
  
    if (confirmPasswordInput.value.trim() === '') {
      alert('Please confirm your password.');
      return false;
    }
  
    if (passwordInput.value !== confirmPasswordInput.value) {
      alert('Password and confirm password do not match.');
      return false;
    }
  
    return true;
  }


  const searchInput = document.getElementById('searchInput');
  const categoryList = document.getElementById('categoryList');
  const categories = categoryList.getElementsByClassName('category');
  
  searchInput.addEventListener('keyup', function(event) {
    const searchTerm = event.target.value.toLowerCase();
    
    for (let i = 0; i < categories.length; i++) {
      const category = categories[i];
      const text = category.innerText.toLowerCase();
      
      if (text.includes(searchTerm)) {
        category.classList.add('show');
      } else {
        category.classList.remove('show');
      }
    }
  });


  function goToLandingPage1( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/";
   }

   function goToLandingPage2( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/signup";
   }

   function goToLandingPage3( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/about";
   }



   function goToLandingPage5( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/about";
   }


   function goToLandingPage7( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/about";
   }

   function goToLandingPage14( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/login";
   }


   function goToLandingPage12( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/signup";
   }


   function goToLandingPage96( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/login_buyer";
   }


   function goToLandingPage8( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/login";
   }


   function goToLandingPage1( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/";

   }


   function goToLandingPage9( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/sell_review";
   }

   function goToLandingPage10( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/volvo";
   }



   function goToLandingPage11( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/car_sell";
   }

   function goToLandingPage15( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/login";
   }


   function goToLandingPage16( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/login_buyer";
   }


   function goToLandingPage17( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/car_sell";
   }


  


   function goToLandingPage6( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/signup_buyer";
   }


   function goToLandingPage99( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/view_items";
   }


   function goToLandingPage60( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
  // Use a relative path so the app works on any host/port (dev or production)
  window.location.href = "/retrieve_seller";
   }

   function goToLandingPage45( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/about";
   }


   function goToLandingPage66( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/buyer_message";
   }

   function goToLandingPage67( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/review";
   }

   function goToLandingPage25( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/review_display12";
   }


   function goToLandingPage50( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/";
   }

   function goToLandingPage58( ) {
    // Replace the URL "/landing-page" with the actual URL or route of the landing page
   window.location.href = "https://driven-dynamics.onrender.com/review";
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





   






   


   


 

   





  




 