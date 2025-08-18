// Typewriter effect for headings
document.addEventListener("DOMContentLoaded", function () {
    let text = "🚀 Cyber Security Scanner - Sci-Fi Mode Activated...";
    let i = 0;
    let speed = 75;
    let target = document.querySelector("h1");

    function typeWriter() {
        if (i < text.length) {
            target.innerHTML += text.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
    }
    target.innerHTML = "";
    typeWriter();
});

// Fake animated logs
function addLog(message) {
    let logBox = document.querySelector(".logs");
    let time = new Date().toLocaleTimeString();
    logBox.innerHTML += `[${time}] ${message}<br>`;
    logBox.scrollTop = logBox.scrollHeight;
}

// Example log updates
setTimeout(() => addLog("🔍 Initializing scanner..."), 1000);
setTimeout(() => addLog("⚡ Ports scanning started..."), 2000);
setTimeout(() => addLog("📡 Collecting results..."), 4000);
setTimeout(() => addLog("✅ Report generated successfully!"), 6000);
