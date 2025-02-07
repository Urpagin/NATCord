// Wait until DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    // Get elements
    const menuBtn = document.getElementById("menuBtn");
    const menuDropdown = document.getElementById("menuDropdown");
    const usernameDisplay = document.getElementById("usernameDisplayDropdown");

    // Toggle the hamburger dropdown menu
    menuBtn.addEventListener("click", (event) => {
        menuDropdown.style.display =
            menuDropdown.style.display === "block" ? "none" : "block";
        event.stopPropagation(); // Prevent the click from bubbling up
    });

    // Collapse the dropdown if clicking outside of it
    document.addEventListener("click", (event) => {
        if (!menuBtn.contains(event.target) && !menuDropdown.contains(event.target)) {
            menuDropdown.style.display = "none";
        }
    });

    // Helper function to get a cookie by name
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(";");
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i].trim();
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length);
        }
        return null;
    }

    // Update the displayed username in the menu from the cookie
    const username = getCookie("username") || "Username";
    if (usernameDisplay) {
        usernameDisplay.textContent = username;
    }
});
