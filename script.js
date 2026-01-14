function sendMessage() {
    let input = document.getElementById("user-input");
    let msg = input.value;
    if (msg === "") return;

    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<div class="user">${msg}</div>`;
    input.value = "";

    fetch("/get", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ msg: msg })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += `<div class="bot">${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}
