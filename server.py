from flask import Flask, request
from flask_cors import CORS
import os
import torch
from PIL import Image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model nhận diện chữ số
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', source='local')

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

    # Nhận diện bằng YOLOv5
    results = model(image_path)
    labels = results.pandas().xyxy[0]['name'].tolist()  # lấy tên các object nhận diện được
    print("Detected:", labels)

    return f'Detected digits: {labels}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
