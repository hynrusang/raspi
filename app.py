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
        time.sleep(1)
        """
        ret, frame = camera.read()
        if ret: 
            cv2.imwrite("static/latest.jpg", frame)
            socketio.emit("onPhotoReady")
            time.sleep(1)
        """

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.start_background_task(cameraRelease)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, log_output=True)
