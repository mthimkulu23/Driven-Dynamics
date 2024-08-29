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
       window.location.href = "https://driven-dynamics.onrender.com/catelog_buyer";
       }
});



     
