document.addEventListener("DOMContentLoaded", function() {
  const chatButton = document.getElementById("chat-button");
  const chatWidget = document.getElementById("chat-widget");
  const closeChat = document.getElementById("close-chat");
  const sendBtn = document.getElementById("send-btn");
  const chatInput = document.getElementById("chat-input");
  const chatMessages = document.getElementById("chat-messages");

  // Toggle chat from launcher icon
  chatButton.addEventListener("click", () => {
    chatWidget.classList.toggle("hidden");
  });

  // Close chat from X button
  closeChat.addEventListener("click", (e) => {
   e.stopPropagation();
   chatWidget.classList.add("hidden");
 });

  // closeChat.addEventListener("click", (e) => {
  //   console.log("X clicked");
  //   chatWidget.classList.add("hidden");
  // });

  // Send message
  sendBtn.onclick = sendMessage;
  chatInput.addEventListener("keypress", e => {
    if (e.key === "Enter") sendMessage();
  });

  async function sendMessage() {
    const userText = chatInput.value.trim();
    if (!userText) return;

    addMessage("You", userText);
    chatInput.value = "";

    const typingMessage = addMessage("AskLee", "Typing...");

    const response = await fetch("http://127.0.0.1:8000/chatbot/", {  // fetches the FastAPI - needs to be running to work.
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ message: userText})
  })

  const data = await response.json();
//  console.log(data)  // Allows the for the log to be relayed to the site. 
  
 // setTimeout(() => {  // Replaced with the asynchronous nature of sendMessage() function...
  const botReply = data.response;  // dot annotate the fetch
  addMessage("AskLee AI 🌱", botReply);
   }

  function addMessage(sender, text) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.textContent = text;
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return msg;
  }
});