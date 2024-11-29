from flask import Flask, render_template
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def cameraRelease():
    ret, frame = camera.read()
    if ret: cv2.imwrite("static/latest.jpg", frame)
    cap.release()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    cameraRelease()
    app.run(host='0.0.0.0', port=5000)
