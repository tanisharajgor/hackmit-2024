from flask import Flask, render_template, Response
import cv2
from ultralytics import YOLO
import threading

app = Flask(__name__)

# Load YOLO model
model = YOLO('./models/yolov8l.pt')  

# Global variables
bounding_boxes = []
labels = []
clicked_info = ""
translation_lock = threading.Lock()

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB (YOLOv8 expects RGB)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform detection
        results = model(img)

        # Process detections
        bounding_boxes.clear()
        labels.clear()
        if results and results[0].boxes is not None:
            detections = results[0].boxes
            for det in detections:
                x1, y1, x2, y2 = det.xyxy[0].tolist()
                conf = det.conf[0].tolist()
                cls = int(det.cls[0].tolist())
                cls = min(cls, len(model.names) - 1)
                label = f'{model.names[cls]}'
                bounding_boxes.append((int(x1), int(y1), int(x2), int(y2)))
                labels.append(label)
                frame = cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                # frame = cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display clicked information if any
        # if clicked_info:
            # frame = cv2.putText(frame, f"Clicked Object: {clicked_info}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/click_event/<int:x>/<int:y>')
def click_event(x, y):
    global clicked_info
    clicked_info = ""
    for i, (box, label) in enumerate(zip(bounding_boxes, labels)):
        x1, y1, x2, y2 = box
        if x1 <= x <= x2 and y1 <= y <= y2:
            clicked_info = label
            return label  # Return the object's label (name)
    return "No object clicked"  # Return this if no object was clicked


if __name__ == "__main__":
    app.run(debug=True)
