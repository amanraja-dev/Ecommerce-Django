// document.addEventListener("DOMContentLoaded", function () {
//     // Dynamically inject loader HTML
//     let loaderHTML = '<div class="loader">' +
//         '<div class="loader-inner"></div>' +
//         '</div>';
//     document.body.insertAdjacentHTML('beforeend', loaderHTML);

//     let loader = document.querySelector(".loader");

//     // Function to handle the loading of the visible part
//     function handleIntersection(entries, observer) {
//         entries.forEach(entry => {
//             if (entry.isIntersecting) {
//                 // Hide the loader when the main content in the viewport is visible
//                 loader.style.display = "none";
//                 observer.disconnect(); // Stop observing once the loader is hidden
//             }
//         });
//     }

//     // Use IntersectionObserver to check when the main content is visible
//     let observer = new IntersectionObserver(handleIntersection, {
//         root: null, // Use the viewport as the root
//         threshold: 0.1 // Adjust threshold to trigger when 10% of the element is in view
//     });

//     // Start observing the main content
//     let mainContent = document.querySelector('#main-content');
//     if (mainContent) {
//         observer.observe(mainContent);
//     } else {
//         // Fallback: If no main content element, hide loader on window load
//         window.addEventListener("load", function () {
//             loader.style.display = "none";
//         });
//     }

//     // Dynamically inject scroll-to-top button HTML
//     let scrollToTopBtnHTML = '<button id="scrollToTopBtn" onclick="scrollToTop()">Top</button>';
//     document.body.insertAdjacentHTML('beforeend', scrollToTopBtnHTML);

//     // Show or hide the scroll-to-top button based on scroll position
//     window.addEventListener('scroll', function () {
//         var scrollToTopBtn = document.getElementById('scrollToTopBtn');
//         if (window.pageYOffset > 100) {
//             scrollToTopBtn.style.display = 'block';
//         } else {
//             scrollToTopBtn.style.display = 'none';
//         }
//     });
// });

// Scroll to top function
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
    value = value.replace(/[^a-zA-Z0-9@.\_]/g, '');  // Remove characters other than alphabets, numbers, @, ., -, _, +
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

// password vivibility with toggle 
document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.querySelector('#togglePassword');
    const passwordInput = document.querySelector('#inputPassword');

    togglePassword.addEventListener('click', function () {
        // Toggle the type attribute
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);

        // Toggle the button text
        this.textContent = type === 'password' ? 'lock' : 'lock_open';
    });
});


// Adjust the alignment of the last row's items
const container = document.querySelector('.container');

function adjustLastRow() {
    const items = container.querySelectorAll('.item');
    const itemsPerRow = 4; // Number of items per row
    const itemCount = items.length;
    
    // Remove custom alignment classes
    items.forEach(item => item.classList.remove('align-left'));

    // Find the number of items in the last row
    const itemsInLastRow = itemCount % itemsPerRow;

    if (itemsInLastRow !== 0 && itemsInLastRow < itemsPerRow) {
        // Align items to the left in the last row if it has less than the expected count
        for (let i = itemCount - itemsInLastRow; i < itemCount; i++) {
            items[i].classList.add('align-left');
        }
    }
}

// Add a class for left alignment
const style = document.createElement('style');
style.innerHTML = `
    .align-left {
        margin-left: 0 !important;
    }
`;
document.head.appendChild(style);

// Call the function initially 
adjustLastRow();

// If items change dynamically, you can call adjustLastRow() again


document.addEventListener('DOMContentLoaded', () => {
    let path = window.location.pathname;

    let menuItems = document.querySelectorAll('.bottom_tab ul li a');

    menuItems[0].classList.add('active');

    // Function to set the active menu item based on the current path
    function setActiveMenuItem(menuItems) {
        menuItems.forEach(function (item) {
            item.classList.remove('active');
            if (item.getAttribute('href') === path) {
                item.classList.add('active');
            }
        });
    }

    // Call the function to set the active menu item
    setActiveMenuItem(menuItems);
});



