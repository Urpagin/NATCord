import { globalUser } from './globals.js';


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
        console.log(poll_resp);

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

            let user = msg.user;
            let userColor = user.color_hex;
            let userIconB64 = user.icon_b64;
            let username = user.username;

            // If the server sends us back the message we sent it,
            // do not append it.
            if (!sentMessageUuids.has(uuid)) {
                appendMessage(username, content);
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


function updateClientList(clients) {
    // Get the sidebar container.
    const sidebar = document.querySelector('.online-sidebar');

    // Clear the current content.
    sidebar.innerHTML = "";

    // Create and append a header showing active clients count.
    const header = document.createElement('h2');
    header.textContent = `Online (${clients.active_clients_count})`;
    sidebar.appendChild(header);

    // Append each active (online) user.
    clients.active_users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.classList.add('online-user');

        // Create a green dot.
        const dot = document.createElement('span');
        dot.style.display = 'inline-block';
        dot.style.width = '10px';
        dot.style.height = '10px';
        dot.style.borderRadius = '50%';
        dot.style.backgroundColor = 'green';
        dot.style.marginRight = '8px';

        // Create the username element.
        const usernameSpan = document.createElement('span');
        usernameSpan.textContent = user;

        // Append the dot and username to the container.
        userDiv.appendChild(dot);
        userDiv.appendChild(usernameSpan);
        sidebar.appendChild(userDiv);
    });

    // If there are inactive users, create a divider and list them.
    if (clients.inactive_users && clients.inactive_users.length > 0) {
        // Divider.
        const divider = document.createElement('hr');
        divider.style.margin = '10px 0';
        sidebar.appendChild(divider);

        // Offline header.
        const offlineHeader = document.createElement('h3');
        offlineHeader.textContent = 'Offline';
        offlineHeader.style.fontSize = '0.9em';
        offlineHeader.style.color = '#888';
        sidebar.appendChild(offlineHeader);

        // Append each inactive user.
        clients.inactive_users.forEach(user => {
            const userDiv = document.createElement('div');
            userDiv.classList.add('offline-user');

            // Create a grey dot.
            const dot = document.createElement('span');
            dot.style.display = 'inline-block';
            dot.style.width = '10px';
            dot.style.height = '10px';
            dot.style.borderRadius = '50%';
            dot.style.backgroundColor = 'grey';
            dot.style.marginRight = '8px';

            // Create the username element, styled in grey.
            const usernameSpan = document.createElement('span');
            usernameSpan.textContent = user;
            usernameSpan.style.color = 'grey';

            // Append the dot and username.
            userDiv.appendChild(dot);
            userDiv.appendChild(usernameSpan);
            sidebar.appendChild(userDiv);
        });
    }

    console.log("Updated client list:", clients);
}







// ---

// Pre-assigned colors for some usernames.
const usernameColors = {
    "Alice": "#ff5555",
    "Bob": "#55ff55",
    "Charlie": "#5555ff",
    "ZOZOZO": "#5555ff",
};

// Define the current username (this value can be inserted server-side).
// Return a color for the username. If none is pre-assigned, generate one.
function getUsernameColor(username) {
    if (usernameColors[username]) return usernameColors[username];
    // Generate a random color.
    const color = '#' + Math.floor(Math.random() * 16777215).toString(16);
    usernameColors[username] = color;
    return color;
}

/// Appends a message to the message history.
function appendMessage(username, message) {
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
    usernameSpan.style.color = getUsernameColor(username);
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
    const message = input.value;
    const uuid = crypto.randomUUID();
    if (!message.trim()) return; // Ignore empty messages

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
            appendMessage(globalUser.username, message);
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
});








