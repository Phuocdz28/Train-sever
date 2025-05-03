from flask import Flask, request
import os
import torch
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

@app.route('/')
def home():
    return 'Server is online!'

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image part', 400

    image = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, 'latest.jpg')
    image.save(image_path)

    # Dự đoán bằng YOLO
    results = model(image_path)
    labels = results.pandas().xyxy[0]['name'].tolist()
    print("Detected:", labels)

    if 'person' in labels:
        return 'person', 200
    return 'no_person', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
