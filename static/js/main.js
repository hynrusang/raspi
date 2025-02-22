// 소켓 연결
const socket = io({
    transports: ['websocket']
});

// 이벤트를 링크할 Dom 타겟팅
const img = document.querySelector(".camera-section img")
const footer = document.querySelector("footer");
const toggle = document.querySelector(".toggle");

let ledMode = "수동"

// 소켓 연결 시, 서버측과의 사진 통신
socket.on("connect", () => {
    socket.emit("eRequestPhoto")
    img.onload = () => socket.emit("eRequestPhoto")
});
socket.on("eResponsePhoto", () => img.src = `static/latest.jpg?${new Date().getTime()}`)

// 서버로부터 받은 정보 출력
socket.on("eInfo", text => {
    const newInfo = document.createElement("div");
    newInfo.classList.add("info-item");
    newInfo.textContent = text;
    
    footer.append(newInfo);

    const infoItems = document.querySelectorAll(".info-item");
    if (infoItems.length > 3) infoItems[0].remove();
})

// LED 관련 모듈 토글
function toggleMode() {
    if (ledMode === "수동") {
        ledMode = "자동";
        toggle.classList.add("conditional");
    } else {
        ledMode = "수동";
        toggle.classList.remove("conditional");
    }
    socket.emit("eToggleLedMode", ledMode)
}

// 자동 조작 설정 전송
function applyCondition() {
    const values = document.querySelectorAll("#led_condition input");
    const options = document.querySelectorAll("#led_condition select");
    socket.emit("eApplyLedCondition", {
        light: {
            value: values[0].value,
            condition: options[0].value
        },
        temp: {
            value: values[1].value,
            condition: options[1].value
        },
        humi: {
            value: values[2].value,
            condition: options[2].value
        }
    });
}

// 사진을 클라이언트에 저장하는 함수
function saveImg() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const timestamp = `${year}-${month}-${day}_${hours}-${minutes}`;

    const link = document.createElement("a");
    link.href = img.src;
    link.download = `image_${timestamp}.jpg`;
    link.click();
}