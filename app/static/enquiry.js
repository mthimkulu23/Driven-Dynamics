document.getElementById('inquiry-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: form.method,
            body: new URLSearchParams(formData)
        });

        if (response.ok) {
            document.getElementById('popup').style.display = 'block';
        } else {
            alert('Failed to submit enquiry');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while submitting the enquiry');
    }
});

document.getElementById('close-popup').addEventListener('click', function() {
    document.getElementById('popup').style.display = 'none';

    {
        // Replace the URL "/landing-page" with the actual URL or route of the landing page
       window.location.href = "http://127.0.0.1:5000/catelog_buyer";
       }
});




function goToLandingPage17(){

    window.location.href = "http://127.0.0.1:5000/enquire"
}


function goToLandingPage2(){

    window.location.href = "http://127.0.0.1:5000/catelog_buyer"
}


function goToLandingPage28(){

    window.location.href = "http://127.0.0.1:5000/review_display12"
}




function goToLandingPage1(){

    window.location.href = "http://127.0.0.1:5000/"
}


     
