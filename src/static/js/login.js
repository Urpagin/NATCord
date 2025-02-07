// Helper function to set a cookie with a given name, value, and expiration in days.
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

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
