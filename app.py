from flask import Flask, render_template
from flask_socketio import SocketIO
from adafruit_htu21d import HTU21D
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import busio
import cv2

app = Flask(__name__)
socketio = SocketIO(app)

camera = cv2.VideoCapture(0)
ledPin = 6
isConnect = 0

# 데이터 구조
data = {
    "led": {
        "state": "off",
        "mode": "수동",
        "condition": {
            "temp": {"standard": None, "condition": None},
            "humi": {"standard": None, "condition": None},
            "light": {"standard": None, "condition": None}
        }
    },
    "temp": None,
    "humi": None,
    "light": None
}

# GPIO 및 센서 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
sensor = HTU21D(busio.I2C(3, 2))
mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

if not camera.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

# 자동 LED 제어 함수
def evaluateCondition(conditions):
    for key, details in conditions.items():
        value = data.get(key)
        standard = details["standard"]
        option = details["condition"]
        
        if value is None or standard is None or option is None:
            continue
        if option == "이상" and value < standard:
            return False
        elif option == "이하" and value > standard:
            return False
    return True

# 특정 시간마다 정보를 클라이언트에게 전송
def sendInfo():
    while True:
        if (isConnect == 0): return
        
        data["temp"] = round(float(sensor.temperature), 1)
        data["humi"] = round(float(sensor.relative_humidity), 1)
        data["light"] = float(mcp.read_adc(0))

        if data["led"]["mode"] == "자동":
            is_condition_met = evaluateCondition(data["led"]["condition"])
            GPIO.output(ledPin, GPIO.HIGH if is_condition_met else GPIO.LOW)
            data["led"]["state"] = "on" if is_condition_met else "off"

        socketio.emit("eInfo", f"온도: {data['temp']}°C, 습도: {data['humi']}%, 조도: {data['light']}")
        socketio.sleep(1)

@socketio.on("connect")
def onConnect():
    global isConnect
    isConnect = 1
    socketio.start_background_task(sendInfo)

@socketio.on("disconnect")
def onDisconnect():
    global isConnect
    isConnect = 0

# 소켓 이벤트: 사진 요청
@socketio.on('eRequestPhoto')
def requestPhoto():
    ret, frame = camera.read()
    if ret:
        cv2.imwrite("static/latest.jpg", frame)
        socketio.emit("eResponsePhoto")

# 소켓 이벤트: LED 상태 토글
@socketio.on('eToggleLed')
def toggleLed():
    if data["led"]["mode"] != "수동":
        socketio.emit("eInfo", "LED 모드를 수동으로 설정해주세요.")
        return

    data["led"]["state"] = "on" if data["led"]["state"] == "off" else "off"
    GPIO.output(ledPin, GPIO.HIGH if data["led"]["state"] == "on" else GPIO.LOW)
    socketio.emit("eInfo", f"LED 상태가 {data['led']['state']}로 변경되었습니다.")

# 소켓 이벤트: LED 모드 변경
@socketio.on('eToggleLedMode')
def toggleLedMode(mode):
    data["led"]["mode"] = mode
    socketio.emit("eInfo", f"LED 모드가 {data['led']['mode']}으로 설정되었습니다.")

# 소켓 이벤트: 조건 설정
@socketio.on("eApplyLedCondition")
def applyLedCondition(conditions):
    for key in ["temp", "humi", "light"]:
        if key in conditions:
            data["led"]["condition"][key]["standard"] = float(conditions[key]["value"]) if (conditions[key]["value"] != "") else None 
            data["led"]["condition"][key]["condition"] = conditions[key]["condition"]
    socketio.emit("eInfo", "조건이 성공적으로 설정되었습니다.")

# 기본 라우팅
@app.route("/")
def index():
    return render_template("index.html")

# 앱 실행
if __name__ == "__main__":
    try:
        socketio.run(app, host="0.0.0.0", port=5000, log_output=True)
    finally:
        GPIO.cleanup()
        camera.release()
        print("카메라 및 핀 초기화 완료.")
