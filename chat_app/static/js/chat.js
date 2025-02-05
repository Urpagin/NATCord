function testFunc() {
    console.log("hallo");
    alert("button clikced!");
}

// Simple polling. We could have used SSE (Server-Sent Events) but there are some problems with Flask or something
// It's a tad bit difficult.
let lastTimestamp = Math.floor(Date.now() / 1000); // Initialize with the current time
let initialReq = true;

async function fetchMessages() {
    try {
        let response;
        if (initialReq) {
            initialReq = false;
            // Correctly concatenate query parameters using `&`
            response = await fetch(`/poll?last_timestamp=${lastTimestamp}&get_history=1`);
        } else {
            // Fetch messages using lastTimestamp
            response = await fetch(`/poll?last_timestamp=${lastTimestamp}`);
        }
        const messages = await response.json();
        

        // Append only new messages
        messages.forEach(msg => {
            appendMessage("eclipsoss", msg);
        });

        // Update lastTimestamp to the most recent message received
        if (messages.length > 0) {
            lastTimestamp = Math.floor(Date.now() / 1000); // Initialize with the current time
        }
    } catch (error) {
        console.error("Error fetching messages:", error);
    }
}

// Poll every 2 seconds, meaning lastTimestamp updates continuously
setInterval(fetchMessages, 500);

// Initial fetch ensures messages load immediately
fetchMessages();



/// Appends a message to the message list on the message history.
function appendMessage(friendName, message) {
    const messageContainer = document.querySelector('.private-messages');

    // Ensure the chat header is added only once
    if (!document.querySelector('.private-messages h2')) {
        const header = document.createElement('h2');
        header.textContent = `Messages with ${friendName}`;
        messageContainer.appendChild(header);
    }

    // Create a new message div and append it
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    messageDiv.style.padding = '0.5rem';
    messageDiv.style.marginBottom = '0.5rem';
    messageDiv.style.backgroundColor = '#4f545c';
    messageDiv.style.borderRadius = '5px';

    messageContainer.appendChild(messageDiv);

    // scroll to the bottom
    messageContainer.scrollTop = messageContainer.scrollHeight;
}



async function sendMessage(message) {
    if (!message.trim()) return; // Ignore empty messages

    const timestamp = Math.floor(Date.now() / 1000); // Get current UNIX timestamp

    try {
        const response = await fetch('/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'message': message,
                'timestamp': timestamp
            })
        });

        if (!response.ok) {
            console.error("Failed to send message:", response.statusText);
        } else {
            //appendMessage("bla bla", message);
        }
    } catch (error) {
        console.error("Error sending message:", error);
    }
}



// only when the page is loaded
document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.getElementById("messageInput");
    
    if (inputField) {  // Ensure the input field exists
        inputField.addEventListener("keydown", function(event) {
            if (event.key === "Enter" && this.value.trim() !== "") {
                sendMessage(this.value);
                this.value = ""; // Clear input
            }
        });
    } else {
        console.error("Error: #messageInput not found!");
    }
});
