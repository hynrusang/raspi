function updateFooter() {
    const footer = document.querySelector("footer");
    
    // 새 정보 생성
    const newInfo = document.createElement("div");
    newInfo.classList.add("info-item");
    newInfo.textContent = `실시간 정보: ${new Date().toLocaleTimeString()}`;
    
    // 새 정보 추가 (아래쪽에 표시)
    footer.append(newInfo);
    
    // 정보가 5개를 초과하면 가장 오래된 정보 삭제
    const infoItems = document.querySelectorAll(".info-item");
    if (infoItems.length > 3) {
        infoItems[0].remove();
    }
}

// 2초마다 정보 갱신 (데모용)
setInterval(updateFooter, 1000);

let currentMode = "manual"; // 초기 모드는 수동

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

function toggleLed() {
    if (currentMode !== "manual") {
        alert("수동 모드를 활성화하세요.");
        return;
    }
    alert("LED를 수동으로 제어했습니다.");
}

function applyConditions() {
    if (currentMode !== "conditional") {
        alert("조건부 모드를 활성화하세요.");
        return;
    }
    const temperature = document.getElementById("temperature-value").value;
    const temperatureCondition = document.getElementById("temperature-condition").value;
    const brightness = document.getElementById("brightness-value").value;
    const brightnessCondition = document.getElementById("brightness-condition").value;

    const conditionSummary = [];
    if (temperature) conditionSummary.push(`온도 ${temperatureCondition} ${temperature}`);
    if (brightness) conditionSummary.push(`조도 ${brightnessCondition} ${brightness}`);

    if (conditionSummary.length > 0) {
        alert(`조건이 설정되었습니다: ${conditionSummary.join(", ")}`);
    } else {
        alert("조건을 입력해주세요.");
    }
}