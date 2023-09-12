from flask import Flask, render_template, url_for, Response, request
import cv2
from cv2 import data
from deepface import DeepFace




def generate_frames():
    global camera
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while True:
        try:
            success, frame = camera.read()  # read the camera frame
            results = DeepFace.analyze(frame, actions=['emotion'])  # analyze the frame for emotion

            if 'emotion' in results[0]:
                emotion = results[0]['emotion']
                for key, value in emotion.items():
                    if value > 50:  # it`s something like a measurement accuracy/ if the value is less than 50% (weak emotion) the app will not show the emotion
                        cv2.putText(frame, key, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if face_cascade.empty():
                continue
            else:
                # detect faces in the frame
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


        # if case of face now found the app will start the camera without face detection
        except ValueError:
            success, frame = camera.read()  # read the camera frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title= 'Main Page')


@app.route('/analysis')
def analysis():
    return render_template('analysis.html', title='Analysis Page')


@app.route('/about')
def about():
    return render_template('about.html', title='About Page')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
