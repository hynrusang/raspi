const socket = io({
    transports: ['websocket']
});
const img = document.querySelector(".camera-section img")
const ledToggleBtn = document.querySelector(".control-section button")
const footer = document.querySelector("footer");
const toggle = document.querySelector(".toggle");

let ledMode = "수동"

socket.on("connect", () => {
    socket.emit("ePhotoRequest")
    socket.emit("eLedModeToggle", {state: ledMode})
    img.onload = () => socket.emit("ePhotoRequest")
    ledToggleBtn.onclick = () => socket.emit("eLedToggle")
});
socket.on("ePhotoReady", () => img.src = `static/latest.jpg?${new Date().getTime()}`)
socket.on("onInfo", data => {
    const newInfo = document.createElement("div");
    newInfo.classList.add("info-item");
    newInfo.textContent = data.message;
    
    footer.append(newInfo);

    const infoItems = document.querySelectorAll(".info-item");
    if (infoItems.length > 3) infoItems[0].remove();
})

function toggleMode() {
    if (ledMode === "수동") {
        ledMode = "조건";
        toggle.classList.add("conditional");
        socket.emit("eLedModeToggle", {state: ledMode})
    } else {
        ledMode = "수동";
        toggle.classList.remove("conditional");
        socket.emit("eLedModeToggle", {state: ledMode})
    }
}