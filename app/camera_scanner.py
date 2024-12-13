import cv2
import numpy as np
import os
import time
from flask import Blueprint, Response

# Define the Blueprint for the camera scanner
camera_app = Blueprint("camera", __name__)

CAPTURE_FOLDER = "captured_images"
if not os.path.exists(CAPTURE_FOLDER):
    os.makedirs(CAPTURE_FOLDER)

# Function to detect the document contour in the frame
def detect_document_contour(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            return approx
    return None

# Function to guide the user on how to align the document
def guide_user(approx, frame_width, frame_height):
    cx, cy = np.mean(approx[:, 0, :], axis=0)
    
    if cx < frame_width * 0.3:
        return "Move paper to the right."
    elif cx > frame_width * 0.7:
        return "Move paper to the left."
    elif cy < frame_height * 0.3:
        return "Move paper down."
    elif cy > frame_height * 0.7:
        return "Move paper up."
    else:
        return "Paper aligned. Capturing..."

# Function to process each frame and detect/document the scan
def process_frame(frame, last_capture_time, capture_delay=1):
    frame_height, frame_width = frame.shape[:2]
    approx = detect_document_contour(frame)
    
    if approx is not None:
        guide_message = guide_user(approx, frame_width, frame_height)
        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
        cv2.putText(frame, guide_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        current_time = time.time()
        if guide_message == "Paper aligned. Capturing..." and current_time - last_capture_time > capture_delay:
            filename = f"{CAPTURE_FOLDER}/captured_image_{int(current_time)}.jpg"
            cv2.imwrite(filename, frame)
            last_capture_time = current_time
    else:
        cv2.putText(frame, "No document detected. Adjust paper.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    return frame, last_capture_time

# Route to stream the camera feed and process the frames
@camera_app.route('/camera')
def camera_feed():
    def generate():
        cap = cv2.VideoCapture(0)
        last_capture_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame, last_capture_time = process_frame(frame, last_capture_time)
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
        
        cap.release()
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
