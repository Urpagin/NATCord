import { setCookie } from './globals.js';


// Function to read the username from the input and set the cookie.
function setUsernameCookie() {
    const usernameInput = document.getElementById("username");
    const username = usernameInput.value;
    // Set the "username" cookie for 7 days.
    setCookie("username", username, 7);
    console.log("Username cookie set:", document.cookie);
}

// Bind the click event to the submit button after the DOM is loaded.
document.addEventListener('DOMContentLoaded', () => {
    const submitButton = document.querySelector('button[type="submit"]');
    submitButton.addEventListener('click', setUsernameCookie);
});
