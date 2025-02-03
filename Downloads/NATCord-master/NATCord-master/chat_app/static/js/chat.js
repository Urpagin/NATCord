document.addEventListener("DOMContentLoaded", function() {
    const profileIcon = document.getElementById("profileIcon");
    const profileBox = document.getElementById("profileBox");
    const closeProfile = document.getElementById("closeProfile");

    // Quand l'icône est cliquée, on toggle la classe .show
    profileIcon.addEventListener("click", function() {
        profileBox.classList.toggle("show");
    });

    // Fermer la box quand on clique sur "Fermer"
    closeProfile.addEventListener("click", function() {
        profileBox.classList.remove("show");
    });
});
