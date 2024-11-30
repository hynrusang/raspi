from flask import Flask, render_template
from flask_socketio import SocketIO
from adafruit_htu21d import HTU21D
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import threading
import busio
import time
import cv2

app = Flask(__name__)
socketio = SocketIO(app)
camera = cv2.VideoCapture(0)

lock = 0
ledPin = 6
ledMode = "수동"
ledState = "off"
data = {
    "temp": 0,
    "humi": 0,
    "light": 0
}

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
sensor = HTU21D(busio.I2C(3, 2))
mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

if not camera.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

def syncLedState():
    return

def sendInfo():
    while True:
        data["temp"] = round(float(sensor.temperature), 1)
        data["humi"] = round(float(sensor.relative_humidity), 1)
        data["light"] = float(mcp.read_adc(0) / 10)
        socketio.emit("onInfo", {"message": f"온도: {data['temp']}, 습도: {data['humi']}, 조도: {data['light']}"})
        socketio.sleep(1)

@socketio.on("connect")
def initSocket():
    global lock

    if lock == 0:  # 다른 클라이언트가 없으면 연결 허용
        lock = 1
        socketio.start_background_task(sendInfo)
    else: disconnect()

@socketio.on("disconnect")
def handle_disconnect():
    global lock
    if lock == 1: lock = 0


@socketio.on('ePhotoRequest')
def requestPhoto():
    ret, frame = camera.read()
    if ret:
        cv2.imwrite("static/latest.jpg", frame)
        socketio.emit("ePhotoReady")

@socketio.on('eLedToggle')
def toggleLed():
    if (ledMode != "수동"):
        socketio.emit("onInfo", {"message": f"LED 모드를 수동으로 변경해주세요."})
        return

    global ledState
    if ledState == "off":
        GPIO.output(ledPin, GPIO.HIGH)  # LED 켜기
        ledState = "on"
    else:
        GPIO.output(ledPin, GPIO.LOW)  # LED 끄기
        ledState = "off"
    socketio.emit("onInfo", {"message": f"LED 상태를 {ledState}(으)로 변경했습니다."})

@socketio.on('eLedModeToggle')
def ledModeToggle(data):
    global ledMode
    ledMode = data.get("state")
    socketio.emit("onInfo", {"message": f"LED 모드를 {ledMode}으로 변경했습니다."})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    try:
        socketio.run(app, host='0.0.0.0', port=5000, log_output=True)
    finally:
        GPIO.cleanup()
        camera.release()
        print("카메라 및 핀 초기화 완료.")
