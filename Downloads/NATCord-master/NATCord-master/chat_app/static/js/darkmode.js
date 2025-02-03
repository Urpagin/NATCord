document.addEventListener("DOMContentLoaded", () => {
    const darkModeToggle = document.getElementById("darkModeToggle");
    const settingsButton = document.getElementById("settingsButton");
    const dropdownMenu = document.getElementById("settingsMenu");
    const body = document.body;

    // Vérifie si le mode sombre est activé
    if (localStorage.getItem("dark-mode") === "enabled") {
        body.classList.add("dark-mode");
        darkModeToggle.textContent = "☀️ Mode Clair";
    }

    // Gestion du mode sombre
    darkModeToggle.addEventListener("click", () => {
        body.classList.toggle("dark-mode");
        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("dark-mode", "enabled");
            darkModeToggle.textContent = "☀️ Mode Clair";
        } else {
            localStorage.setItem("dark-mode", "disabled");
            darkModeToggle.textContent = "🌙 Mode Sombre";
        }
    });

    // Gestion de l'affichage du menu déroulant
    settingsButton.addEventListener("click", (e) => {
        e.preventDefault(); // Empêche le comportement par défaut (pas de recharge de page)
        dropdownMenu.classList.toggle("active");
    });

    // Fermer le menu si on clique ailleurs
    document.addEventListener("click", (e) => {
        if (!settingsButton.contains(e.target) && !dropdownMenu.contains(e.target)) {
            dropdownMenu.classList.remove("active");
        }
    });
});
