from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import threading

app = Flask(__name__)
socketio = SocketIO(app)
camera = cv2.VideoCapture(0)

def cameraRelease():
    while True:
        ret, frame = camera.read()
        if ret: 
            cv2.imwrite("static/latest.jpg", frame)
            socketio.emit("onPhotoReady")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    threading.Thread(target=cameraRelease, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
