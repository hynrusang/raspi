from flask import Flask, render_template
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import cv2
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)
camera = cv2.VideoCapture(0)

ledPin = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

ledMode = "수동"
ledState = "off"

if not camera.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

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
    socketio.emit("onInfo", {"message": f"LED 상태를 {ledState}로 변경했습니다."})

@socketio.on('eLedModeToggle')
def ledModeToggle(data):
    global ledMode
    ledMode = data.get("state")
    socketio.emit("onInfo", {"message": f"LED 모드를 {ledMode}로 변경했습니다."})

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
