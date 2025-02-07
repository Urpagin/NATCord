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
