document.addEventListener("DOMContentLoaded", function () {
    // Dynamically inject loader HTML
    let loaderHTML = '<div class="loader">' +
        '<div class="loader-inner"></div>' +
        '</div>';
    document.body.insertAdjacentHTML('beforeend', loaderHTML);

    let loader = document.querySelector(".loader");

    // Hide loader when page content is fully loaded
    window.addEventListener("load", function () {
        loader.style.display = "none";
    });

    // Dynamically inject scroll-to-top button HTML
    let scrollToTopBtnHTML = '<button id="scrollToTopBtn" onclick="scrollToTop()">Top</button>';
    document.body.insertAdjacentHTML('beforeend', scrollToTopBtnHTML);

    // Show or hide the scroll to top button based on scroll position
    window.addEventListener('scroll', function () {
        var scrollToTopBtn = document.getElementById('scrollToTopBtn');
        if (window.pageYOffset > 100) { // Adjust the scroll position as needed
            scrollToTopBtn.style.display = 'block';
        } else {
            scrollToTopBtn.style.display = 'none';
        }
    });
});

// Function to scroll to the top of the page with smooth transition
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}


// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                cookieValue = decodeURIComponent(cookie.substring('csrftoken='.length));
                break;
            }
        }
    }
    return cookieValue;
}

function sendOTP() {
    let email = document.getElementById('email').value;
    // Perform AJAX request to send OTP
    $.ajax({
        type: 'POST',
        url: '/reset-password-otp/', // Update this URL with the correct path,
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        data: { 'email': email },
        success: function (response) {
            if (response.success) {
                // OTP sent successfully
                document.getElementById('otpSection').style.display = 'block';
                document.getElementById('resetPasswordBtn').style.display = 'block';
                document.getElementById('forgetPasswordBtn').style.display = 'none';
            } else {
                // Handle error
                alert('Failed to send OTP. Please try again.');
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            // Handle AJAX error
            alert('Failed to send OTP. Please try again.');
        }
    });
}


function verifyOTP() {
    let otp = document.getElementById('otp').value;
    // Perform AJAX request to verify OTP
    $.ajax({
        type: 'POST',
        url: '{% url "verify_reset_password_otp" %}',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        data: { 'otp': otp },
        success: function (response) {
            if (response.success) {
                // OTP verified successfully
                document.getElementById('resetPasswordBtn').disabled = false;
            } else {
                // Handle error
            }
        }
    });
}


function validateAndTransform(inputElement) {
    let value = inputElement.value;
    value = value.replace(/[^a-zA-Z]/g, ''); // Remove non-alphabetic characters
    value = value.toUpperCase(); // Convert to uppercase
    inputElement.value = value; // Update input field value
}

function validateAndTransformEmail(inputElement) {
    let value = inputElement.value;
    value = value.toLowerCase();    // Convert uppercase letters to lowercase
    value = value.replace(/\s/g, '');  // Remove whitespace
    value = value.replace(/[^a-zA-Z0-9@.\-_+]/g, '');  // Remove characters other than alphabets, numbers, @, ., -, _, +
    inputElement.value = value; // Update input field value
}

function validateNumber(inputElement) {
    let value = inputElement.value;
    value = value.replace(/\D/g, '');
    inputElement.value = value;
}

function validateStateCity(inputElement) {
    let value = inputElement.value;
    value = value.replace(/[^a-zA-Z ]+/g, '');
    value = value.toUpperCase();
    inputElement.value = value;
}

function validatePassword(inputElement) {
    let value = inputElement.value;

    // Check if the password contains at least one uppercase letter
    if (!/[A-Z]/.test(value)) {
        document.getElementById('passwordError').innerText = "Password must contain at least one uppercase letter.";
        return false;
    }

    // Check if the password contains at least one special character
    if (!/[@#$%^&+=]/.test(value)) {
        document.getElementById('passwordError').innerText = "Password must contain at least one special character (@#$%^&+=).";
        return false;
    }

    // Check if the password contains at least one lowercase letter
    if (!/[a-z]/.test(value)) {
        document.getElementById('passwordError').innerText = "Password must contain at least one lowercase letter.";
        return false;
    }

    // Check if the password contains at least one numeric value
    if (!/\d/.test(value)) {
        document.getElementById('passwordError').innerText = "Password must contain at least one numeric value.";
        return false;
    }

    // Check if the password length is at least 8 characters
    if (value.length < 8) {
        document.getElementById('passwordError').innerText = "Password must be at least 8 characters long.";
        return false;
    }

    document.getElementById('passwordError').innerText = ""; // Clear error message if all criteria are met
    return true;
}

function validateForm() {
    if (!validatePassword(document.getElementById('inputPassword4'))) {
        return false; // Prevent form submission if password validation fails
    }
    return true; // Allow form submission if all validations pass
}