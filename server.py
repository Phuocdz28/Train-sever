from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    print("Image received and saved.")
    return 'Image uploaded', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
