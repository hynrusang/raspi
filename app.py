from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import threading
import time

app = Flask(__name__)
camera = cv2.VideoCapture(0)
socketio = SocketIO(app)

@socketio.on('requestPhoto')  # 클라이언트로부터 사진 촬영 요청 처리
def photoPublish():
    print("사진 촬영 요청 수신")
    ret, frame = camera.read()  # 카메라에서 프레임 읽기
    if ret:
        cv2.imwrite("static/latest.jpg", frame)  # 저장
        socketio.sleep(1)
        socketio.emit("responsePhoto")  # 사진 촬영 완료 알림 이벤트 전송
    else:
        print("카메라에서 프레임을 읽지 못했습니다.")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, log_output=True)
