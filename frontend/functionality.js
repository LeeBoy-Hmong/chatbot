document.addEventListener("DOMContentLoaded", function () {
  const chatButton = document.getElementById("chat-button");
  const chatTeaser = document.getElementById("chat-teaser");
  const chatWidget = document.getElementById("chat-widget");
  const closeChat = document.getElementById("close-chat");
  const sendBtn = document.getElementById("send-btn");
  const chatInput = document.getElementById("chat-input");
  const chatMessages = document.getElementById("chat-messages");
  const faqSection = document.getElementById("faq-section");
  const faqButtons = document.querySelectorAll(".faq-btn");

  let isSending = false;

  if (sessionStorage.getItem("chatTeaserDismissed") === "true") {
    chatTeaser.classList.add("hidden");
  }

  chatButton.addEventListener("click", () => {
    chatTeaser.classList.add("hidden");
    sessionStorage.setItem("chatTeaserDismissed", "true");
    chatWidget.classList.toggle("hidden");
  });

  closeChat.addEventListener("click", (e) => {
    e.stopPropagation();
    chatWidget.classList.add("hidden");
  });

  sendBtn.addEventListener("click", sendMessage);

  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  async function sendMessage() {
    if (isSending) return;

    const userText = chatInput.value.trim();
    if (!userText) return;

    isSending = true;
    sendBtn.disabled = true;
    chatInput.disabled = true;

    addMessage("You", userText, "user-message");
    chatInput.value = "";

    const typingMessage = addMessage("AskLee AI", "Thinking...", "bot-message typing");
    const startTime = Date.now();

    try {
      const response = await fetch("http://127.0.0.1:8000/chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userText })
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data = await response.json();
      console.log(data.response);

      const elapsed = Date.now() - startTime;
      const minDelay = 1600;
      const remaining = Math.max(0, minDelay - elapsed);

      setTimeout(async () => {
        typingMessage.classList.remove("typing");
        await renderStreamText(typingMessage, "AskLee AI", data.response, 18);

        isSending = false;
        sendBtn.disabled = false;
        chatInput.disabled = false;
        chatInput.focus();
      }, remaining);

    } catch (error) {
      const elapsed = Date.now() - startTime;
      const minDelay = 800;
      const remaining = Math.max(0, minDelay - elapsed);

      setTimeout(() => {
        typingMessage.classList.remove("typing");
        setMessageText(typingMessage, "AskLee AI", "Sorry, I’m having trouble connecting right now.");
        chatMessages.scrollTop = chatMessages.scrollHeight;

        isSending = false;
        sendBtn.disabled = false;
        chatInput.disabled = false;
        chatInput.focus();
      }, remaining);

      console.error("Chatbot fetch error:", error);
    }
  }
    faqButtons.forEach(button => {
    button.addEventListener("click", () => {
      chatInput.value = button.textContent;
      faqSection.style.display = "none";
      sendMessage();
    });
  });


  function addMessage(sender, text, className) {
    const msg = document.createElement("div");
    msg.className = `message ${className}`;

    const senderDiv = document.createElement("div");
    senderDiv.className = "message-sender";
    senderDiv.textContent = sender;

    const textDiv = document.createElement("div");
    textDiv.className = "message-text";
    textDiv.innerHTML = text;

    msg.appendChild(senderDiv);
    msg.appendChild(textDiv);

    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return msg;
  }

  function setMessageText(element, sender, text) {
    element.innerHTML = "";

    const strong = document.createElement("strong");
    strong.textContent = `${sender}:`;

    const textSpan = document.createElement("span");
    textSpan.textContent = ` ${text}`;

    element.appendChild(strong);
    element.appendChild(textSpan);
  }

  function renderStreamText(element, sender, fullText, speed = 18) {
    return new Promise((resolve) => {
      element.innerHTML = "";

      const senderDiv = document.createElement("div");
      senderDiv.className = "message-sender";
      senderDiv.textContent = sender;

      const textDiv = document.createElement("div");
      textDiv.className = "message-text";

      element.appendChild(senderDiv);
      element.appendChild(textDiv);

      const plainText = fullText.replace(/<[^>]*>/g, "");
      let index = 0;

      function typeNextChar() {
        if (index < plainText.length) {
          textDiv.textContent = plainText.substring(0, index + 1);
          index++;
          chatMessages.scrollTop = chatMessages.scrollHeight;
          setTimeout(typeNextChar, speed);
        } else {
          textDiv.innerHTML = fullText;
          chatMessages.scrollTop = chatMessages.scrollHeight;
          resolve();
        }
      }

      typeNextChar();
    });
  }
});