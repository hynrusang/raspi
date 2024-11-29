from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import threading
import time

app = Flask(__name__)
camera = cv2.VideoCapture(0)
socketio = SocketIO(app)

def cameraRelease():
    while True:
        socketio.emit("onPhotoReady")
        print("onPhotoReady 이벤트 전송")
        time.sleep(1)
        """
        ret, frame = camera.read()
        if ret: 
            cv2.imwrite("static/latest.jpg", frame)
            socketio.emit("onPhotoReady")
            time.sleep(1)
        """

@socketio.on('connect')
def handle_connect():
    print("클라이언트가 성공적으로 연결되었습니다.")


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.start_background_task(cameraRelease)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, log_output=True)
