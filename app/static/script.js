// Tab Switching
document.querySelectorAll("nav button").forEach((button) => {
    button.addEventListener("click", (e) => {
        const tabName = e.target.dataset.tab;

        // Hide all sections
        document.querySelectorAll(".tab-content").forEach((tab) => tab.classList.add("hidden"));

        // Show the clicked tab
        document.getElementById(tabName).classList.remove("hidden");

        // Update active button style
        document.querySelectorAll("nav button").forEach((btn) => btn.classList.remove("active"));
        e.target.classList.add("active");
    });
});

// Toggle Voice Bot
let isVoiceEnabled = false;
document.getElementById("toggle-voice-bot").addEventListener("click", () => {
    isVoiceEnabled = !isVoiceEnabled;
    document.getElementById("toggle-voice-bot").textContent = isVoiceEnabled ? "Disable Voice Bot" : "Enable Voice Bot";
});

// Chatbot Interaction
document.getElementById("chat-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("chat-input").value.trim();
    if (!input) return;

    const chatHistory = document.getElementById("chat-history");
    const userMessage = document.createElement("div");
    userMessage.textContent = `You: ${input}`;
    chatHistory.appendChild(userMessage);

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
    });
    const data = await response.json();
    const botMessage = document.createElement("div");
    botMessage.textContent = `Bot: ${data.response}`;
    chatHistory.appendChild(botMessage);

    document.getElementById("chat-input").value = "";

    // Enable voice output
    if (isVoiceEnabled) {
        const synth = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance(data.response);
        synth.speak(utterance);
    }
});
