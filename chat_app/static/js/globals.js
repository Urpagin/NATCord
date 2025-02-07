export const globalUser = {
  "username": "UNKNOWN",
  "color_hex": "#FFFFFF",
  "icon_b64": null,
};

// Helper function to get a cookie by name.
function getCookie(name) {
  const nameEQ = name + "=";
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    if (cookie.indexOf(nameEQ) === 0) {
      return decodeURIComponent(cookie.substring(nameEQ.length));
    }
  }
  return null;
}

// Function to read the username cookie.
function getUsernameCookie() {
  // See the login.html file for more information about the username cookie.
  return getCookie("username");
}

function setGlobalUser() {
  const username = getUsernameCookie();
  if (username == null) {
    console.error("Error setting the username via the username cookie!!!");
    return;
  }

  globalUser.username = username;
  console.log("Updated globalUser:", globalUser);
}

setGlobalUser();
