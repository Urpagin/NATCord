export async function fetchUserInfo(username) {
  try {
    const response = await fetch(`/user?username=${encodeURIComponent(username)}`);
    if (!response.ok) {
      throw new Error(`Error fetching user info: ${response.statusText}`);
    }
    const userData = await response.json();
    console.log("User Data:", userData);
    return userData;
  } catch (error) {
    console.error("Error:", error);
  }
}

export const globalUser = {
  "username": null,
  "id": null,
  "color_hex": null,
  "creation_time": null,
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

// Helper function to set a cookie with a given name, value, and expiration in days.
export function setCookie(name, value, days) {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Function to read the username cookie.
function getUsernameCookie() {
  // See the login.html file for more information about the username cookie.
  return getCookie("username");
}

export async function setGlobalUser(new_username = null) {
  let username = getUsernameCookie();
  if (username == null) {
    console.error("Error setting the username via the username cookie!!!");
    return;
  }

  if (new_username != null) {
    username = new_username;
    setCookie('username', username, 7);
  }

  // Await the fetchUserInfo result.
  const fetchedUser = await fetchUserInfo(username);
  if (!fetchedUser) return;

  globalUser.username = fetchedUser.username;
  globalUser.id = fetchedUser.id;
  globalUser.color_hex = fetchedUser.color_hex;
  globalUser.creation_time = fetchedUser.creation_time;
  globalUser.icon_b64 = fetchedUser.icon_b64;

  console.log("Updated globalUser:", globalUser);
}

setGlobalUser();
