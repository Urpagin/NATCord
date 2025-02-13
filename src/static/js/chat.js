import { globalUser } from './globals.js';
import { fetchUserInfo } from './globals.js';

// Simple polling. We could have used SSE (Server-Sent Events) but there are some problems with Flask or something
// It's a tad bit difficult.
let lastTimestamp = Math.floor(Date.now() / 1000); // Initialize with the current time
let pollIntervalMs = 500;
let initialReq = true;

let debugCounter = 0;
async function fetchMessages() {
    // Only fetch if the document is visible
    // Optimization simply done!!! (with websockets or SSE this would be optimized by default :/ )
    if (document.hidden) return;


    console.log(`Polling messages... [${debugCounter}] (interval=${pollIntervalMs}ms)`);
    debugCounter++;

    try {
        let response;
        if (initialReq) {
            initialReq = false;
            // Fetch ALL of the messages history (we could slice to optimize if there are 2 million messages)
            response = await fetch(`/poll?last_timestamp=${lastTimestamp}&get_history=1`);
        } else {
            // Fetch messages using lastTimestamp
            response = await fetch(`/poll?last_timestamp=${lastTimestamp}`);
        }
        const poll_resp = await response.json();
        console.log(`Poll response: ${JSON.stringify(poll_resp)}`);

        // List of active clients
        let active_clients = poll_resp.client_activity;

        updateClientList(active_clients);


        // List of messages to append on the frontend
        let messages = poll_resp.messages;

        // Append only new messages
        messages.forEach(msg => {
            let content = msg.content;
            let timestamp = msg.timestamp;
            let uuid = msg.uuid;

            let user = msg.sender;
            let userColor = user.color_hex;
            let userIconB64 = user.icon_b64;
            let username = user.username;

            // If the server sends us back the message we sent it,
            // do not append it.
            if (!sentMessageUuids.has(uuid)) {
                appendMessage(username, content, userColor);
            } else {
                console.log("Calamity avoided!!!!!!");
            }
        });

        // Update lastTimestamp to the most recent message received
        if (messages.length > 0) {
            lastTimestamp = Math.floor(Date.now() / 1000); // Initialize with the current time
        }
    } catch (error) {
        console.error("Error fetching messages:", error);
    }
}



// Poll every .5 seconds, meaning lastTimestamp updates continuously
setInterval(fetchMessages, pollIntervalMs);

// Initial fetch ensures messages load immediately
fetchMessages();


function updateClientList2(clients) {
    // Select the sidebar container for online/offline users.
    const sidebar = document.querySelector('.online-sidebar');
    // Clear any previous content.
    sidebar.innerHTML = "";

    // Create a header element displaying the active user count.
    const header = document.createElement('h2');
    header.textContent = `Online (${clients.active_clients_count})`;
    sidebar.appendChild(header);

    // Helper function to create a user element.
    // 'username' is the user's name.
    // 'color' is the dot's color (e.g., 'green' for active, 'grey' for offline).
    function createUserElement(username, color) {
        const userDiv = document.createElement('div');
        // Add a base class; additional classes (online/offline) can be added later.
        userDiv.classList.add('user');

        // Create a colored dot.
        const dot = document.createElement('span');
        dot.style.display = 'inline-block';
        dot.style.width = '10px';
        dot.style.height = '10px';
        dot.style.borderRadius = '50%';
        dot.style.backgroundColor = color;
        dot.style.marginRight = '8px';

        // Create a span to hold the username.
        const usernameSpan = document.createElement('span');
        usernameSpan.textContent = username;

        // Append the dot and username to the user container.
        userDiv.appendChild(dot);
        userDiv.appendChild(usernameSpan);

        // Attach a click listener that will trigger the user info popup.
        userDiv.addEventListener('click', () => {
            handleUserClick(username);
        });

        return userDiv;
    }

    // Loop over active users and append them with a green dot.
    clients.active_users.forEach(username => {
        const activeUserElement = createUserElement(username, 'green');
        activeUserElement.classList.add('online-user');
        sidebar.appendChild(activeUserElement);
    });

    // If there are offline (inactive) users, create a divider and offline header.
    if (clients.inactive_users && clients.inactive_users.length > 0) {
        const divider = document.createElement('hr');
        divider.style.margin = '10px 0';
        sidebar.appendChild(divider);

        const offlineHeader = document.createElement('h3');
        offlineHeader.textContent = 'Offline';
        offlineHeader.style.fontSize = '0.9em';
        offlineHeader.style.color = '#888';
        sidebar.appendChild(offlineHeader);

        // Loop over offline users and append them with a grey dot.
        clients.inactive_users.forEach(username => {
            const offlineUserElement = createUserElement(username, 'grey');
            offlineUserElement.classList.add('offline-user');
            sidebar.appendChild(offlineUserElement);
        });
    }

    console.log("Updated client list:", clients);
}



/// Appends a message to the message history.
function appendMessage(username, message, userColorHex) {
    const messageContainer = document.querySelector('.message-container');

    // Create a new message div.
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');

    // Create a container for the username.
    const usernameContainer = document.createElement('div');
    usernameContainer.classList.add('username-container');

    const usernameSpan = document.createElement('span');
    usernameSpan.classList.add('username');
    usernameSpan.textContent = username;
    usernameSpan.style.color = userColorHex;
    usernameContainer.appendChild(usernameSpan);

    // Create a container for the message text.
    const messageTextContainer = document.createElement('div');
    messageTextContainer.classList.add('message-text-container');

    const messageText = document.createElement('span');
    messageText.classList.add('text');
    messageText.textContent = message;
    messageTextContainer.appendChild(messageText);


    // Append username above message text.
    messageDiv.appendChild(usernameContainer);
    messageDiv.appendChild(messageTextContainer);
    messageContainer.appendChild(messageDiv);


    // Scroll to the bottom of the message container.
    messageContainer.scrollTop = messageContainer.scrollHeight;
}


// Stores all message UUIDs that we sent.
const sentMessageUuids = new Set();

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    const uuid = crypto.randomUUID();

    if (!message) return; // Ignore empty messages

    const timestamp = Math.floor(Date.now() / 1000); // Current UNIX timestamp

    try {
        const response = await fetch('/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  // Set request as JSON
            },
            body: JSON.stringify({
                content: message,
                user: globalUser,  // No need to manually stringify; fetch does it automatically
                uuid: uuid,
                timestamp: timestamp
            })
        });

        if (!response.ok) {
            console.error("Failed to send message:", response.statusText);
        } else {
            console.log("global useranem" + globalUser.username);
            appendMessage(globalUser.username, message, globalUser.color_hex);
            sentMessageUuids.add(uuid.toString())
            input.value = ''; // Clear input after successful send
        }
    } catch (error) {
        console.error("Error sending message:", error);
    }
}

// Event listener after the DOM has loaded
// Send message on Enter key press.
window.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('messageInput');
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage(globalUser);
        }
    });

    const sendButton = document.getElementById('sendButton');
    sendButton.addEventListener('click', sendMessage);

document.addEventListener('keydown', (event) => {
  const input = document.getElementById('messageInput');
  
  // If the input isn't focused, focus it.
  if (document.activeElement !== input) {
    input.focus();
    
    // Handle printable characters (length of 1).
    if (event.key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
      input.value += event.key;
      event.preventDefault();
    }
    
    // Handle Backspace.
    if (event.key === 'Backspace') {
      input.value = input.value.slice(0, -1);
      event.preventDefault();
    }
    
  }
});


    
});




// Pop-up system:

// Global cache for user info
const userCache = {};

// Called when the mouse enters a user element.
async function handleUserHover(username) {
    // Use cached info if available.
    if (userCache[username]) {
        showUserPopup(userCache[username]);
    } else {
        const userData = await fetchUserInfo(username);
        if (userData) {
            userCache[username] = userData;
            showUserPopup(userData);
        }
    }
}

// Called when the mouse leaves a user element.
function hideUserPopup() {
    const popup = document.getElementById('user-popup');
    if (popup) {
        popup.style.display = 'none';
    }
}


// Formats ugly time in a more readable format:
// DD/MM/YYYY HH:MM:SS
function formatDate(dateString) {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed.
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}


function showUserPopup(userData) {
    let popup = document.getElementById('user-popup');
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'user-popup';
        // Basic styling to match your dark theme:
        popup.style.position = 'fixed';
        popup.style.backgroundColor = '#2f3136';
        popup.style.border = '1px solid #4f545c';
        popup.style.borderRadius = '5px';
        popup.style.padding = '20px';
        popup.style.zIndex = '2000';
        popup.style.boxShadow = '0 0 10px rgba(0,0,0,0.5)';
        document.body.appendChild(popup);
    }
    // Check if there is a valid Base64 image; if not, show "No image".
    let iconHtml = '';
    if (userData.icon_b64 && userData.icon_b64.trim() !== "") {
        iconHtml = `<img src="${userData.icon_b64}" style="width:150px; height:150px; object-fit: contain; border-radius:5px;">`;
    } else {
        iconHtml = `<span style="color:#ccc;">No image</span>`;
    }

    // Populate the popup with user info.
    popup.innerHTML = `
      <h2 style="color: #fff; margin-bottom: 10px;">User Info</h2>
      <p style="color: #fff;"><strong>Username:</strong> ${userData.username}</p>
      <p style="color: #fff;"><strong>ID:</strong> ${userData.id}</p>
      <p style="color: #fff;"><strong>Color:</strong> ${userData.color_hex}</p>
      <p style="color: #fff;"><strong>Created:</strong> ${formatDate(userData.creation_time)}</p>
      <p style="color: #fff;"><strong>Icon:</strong> ${iconHtml}</p>
    `;

    // Position the popup in the center.
    popup.style.top = '50%';
    popup.style.left = '50%';
    popup.style.transform = 'translate(-50%, -50%)';
    popup.style.display = 'block';
}



// Update the online/offline user list in the sidebar.
// Each user element now shows the popup on hover.
function updateClientList(clients) {
    const sidebar = document.querySelector('.online-sidebar');
    sidebar.innerHTML = "";

    // Create header for active users.
    const header = document.createElement('h2');
    header.textContent = `Online (${clients.active_clients_count})`;
    sidebar.appendChild(header);

    // Helper: creates a user element with a dot and username.
    function createUserElement(username, dotColor) {
        const userDiv = document.createElement('div');
        userDiv.classList.add('user');
        userDiv.style.cursor = 'pointer';
        // Add CSS hover highlighting via CSS is recommended, but we keep it simple here.
        userDiv.addEventListener('mouseenter', () => {
            handleUserHover(username);
        });
        userDiv.addEventListener('mouseleave', hideUserPopup);

        const dot = document.createElement('span');
        dot.style.display = 'inline-block';
        dot.style.width = '10px';
        dot.style.height = '10px';
        dot.style.borderRadius = '50%';
        dot.style.backgroundColor = dotColor;
        dot.style.marginRight = '8px';

        const usernameSpan = document.createElement('span');
        usernameSpan.textContent = username;

        userDiv.appendChild(dot);
        userDiv.appendChild(usernameSpan);
        return userDiv;
    }

    // Append active users.
    clients.active_users.forEach(username => {
        const activeUserEl = createUserElement(username, 'green');
        activeUserEl.classList.add('online-user');
        sidebar.appendChild(activeUserEl);
    });

    // Append inactive users (if any).
    if (clients.inactive_users && clients.inactive_users.length > 0) {
        const divider = document.createElement('hr');
        divider.style.margin = '10px 0';
        sidebar.appendChild(divider);

        const offlineHeader = document.createElement('h3');
        offlineHeader.textContent = 'Offline';
        offlineHeader.style.fontSize = '0.9em';
        offlineHeader.style.color = '#888';
        sidebar.appendChild(offlineHeader);

        clients.inactive_users.forEach(username => {
            const offlineUserEl = createUserElement(username, 'grey');
            offlineUserEl.classList.add('offline-user');
            sidebar.appendChild(offlineUserEl);
        });
    }
    console.log("Updated client list:", clients);
}
