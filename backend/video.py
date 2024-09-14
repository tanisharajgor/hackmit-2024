from ultralytics import YOLO
import cv2

# Load the YOLOv8 model
model = YOLO('./models/yolov8l.pt')  # Use the appropriate YOLOv8 model

# Initialize camera
cap = cv2.VideoCapture(0)  # Use the correct camera index (0, 1, etc.)

# Global variables to store bounding boxes, labels, and click status
bounding_boxes = []
labels = []
clicked_info = ""

def click_event(event, x, y, flags, params):
    global clicked_info
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_info = ""
        print(f"Mouse click at: ({x}, {y})")
        for i, (box, label) in enumerate(zip(bounding_boxes, labels)):
            x1, y1, x2, y2 = box
            if x1 <= x <= x2 and y1 <= y <= y2:
                clicked_info = label
                print(f"Object clicked: {label}")
                break

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Convert frame to RGB (YOLOv8 expects RGB)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform detection
    results = model(img)

    # Clear previous bounding boxes and labels
    bounding_boxes.clear()
    labels.clear()

    # Process the detection results
    if results and results[0].boxes is not None:
        detections = results[0].boxes

        for det in detections:
            # Each detection has properties xyxy, confidence, and class
            x1, y1, x2, y2 = det.xyxy[0].tolist()
            conf = det.conf[0].tolist()
            cls = int(det.cls[0].tolist())

            # Ensure class index is within bounds
            cls = min(cls, len(model.names) - 1)

            label = f'{model.names[cls]} {conf:.2f}'
            bounding_boxes.append((int(x1), int(y1), int(x2), int(y2)))
            labels.append(label)
            frame = cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            frame = cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the clicked information on the frame
    if clicked_info:
        frame = cv2.putText(frame, f"Clicked Object: {clicked_info}", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('YOLOv8 Object Detection', frame)

    # Set mouse callback
    cv2.setMouseCallback('YOLOv8 Object Detection', click_event)

    # Exit the video window by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
