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

  function sendMessage() {
    const userText = chatInput.value.trim();
    if (!userText) return;

    addMessage("You", userText);
    chatInput.value = "";

    setTimeout(() => {
      const botReply = fakeBotReply(userText);
      addMessage("GolieXee 🌱", botReply);
    }, 600);
  }

  function addMessage(sender, text) {
    const msg = document.createElement("div");
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function fakeBotReply(input) {
    input = input.toLowerCase();

    if (input.includes("tomato")) {
      return "Tomatoes love full sun and well-drained soil 🍅";
    }
    if (input.includes("hours")) {
      return "We’re open weekends at the flea market — come say hi!";
    }
    if (input.includes("organic")) {
      return "Yes! We grow using organic practices 🌿";
    }

    return "Ask me about vegetables, availability, or market hours!";
  }
});