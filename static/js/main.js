const socket = io({
    transports: ['websocket']
});
const ledMode = "menual"
const img = document.querySelector(".camera-section img")
const ledToggleBtn = document.querySelector(".control-section button")
const footer = document.querySelector("footer");

socket.on("connect", () => {
    socket.emit("ePhotoRequest")
    img.onload = () => socket.emit("ePhotoRequest")
    ledToggleBtn.onclick = () => socket.emit("eLedToggle", {state: ledMode})
});
socket.on("ePhotoReady", () => {
    console.log("사진을 받음.");
    img.src = `static/latest.jpg?${new Date().getTime()}`;
})
socket.on("onInfo", data => {
    const newInfo = document.createElement("div");
    newInfo.classList.add("info-item");
    newInfo.textContent = data.message;
    
    footer.append(newInfo);

    const infoItems = document.querySelectorAll(".info-item");
    if (infoItems.length > 3) infoItems[0].remove();
})

function updateFooter() {
}

function applyConditions() {

}

function toggleMode() {
    const toggle = document.querySelector(".toggle");
    if (currentMode === "manual") {
        currentMode = "conditional";
        toggle.classList.add("conditional");
        alert("LED가 조건부 모드로 전환되었습니다.");
    } else {
        currentMode = "manual";
        toggle.classList.remove("conditional");
        alert("LED가 수동 모드로 전환되었습니다.");
    }
}