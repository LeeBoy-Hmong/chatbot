// Develop a function to grab a user session, if the session is new or not found create a new session.
function SessionID() {
    let sessionID = localStorage.getItem("chat-session-id");  // Attempt to grab the user session.
    // create a randon user session if the session already does not exist.
    if (!sessionID) {
        sessionID = crypto.randomUUID();
        localStorage.setItem("chat-session-id", sessionID);
    }
    // return the session.
    return sessionID;
}

// Create an asyn function to send the message
async function sendMessage(userInput) {
    const sessionID = SessionID()

    const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: userInput,
            session_id: sessionID
        })
    });

    const data = await response.json();

    console.log("Session ID:", sessionID );
    console.log("Backend response:", data);

    return data;
}